import json
import re
from langchain.llms import BaseLLM
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Evaluation(BaseModel):
    is_good_enough: bool = Field(description="Whether the response is good enough")
    reasoning: str = Field(description="Explanation for the evaluation")

class GeneratorOutput(BaseModel):
    content: str = Field(description="The revised tweet content")

class ReflectionChain:
    def __init__(
        self, 
        generator_llm: BaseLLM,
        reflector_llm: BaseLLM,
        evaluator_llm: BaseLLM,
        max_iterations: int = 5,
        generator_role: Optional[str] = None,
        reflector_role: Optional[str] = None,
        evaluator_role: Optional[str] = None,
        topic: Optional[str] = None
    ):
        self.generator_llm = generator_llm
        self.reflector_llm = reflector_llm
        self.evaluator_llm = evaluator_llm
        self.max_iterations = max_iterations
        
        self.generator_system_message = (
            f"You are an expert specialized in {topic}. " if topic else
            "You are an expert. "
        ) + (
            f"Your role is to be a {generator_role}. " if generator_role else
            "Your role is to generate or improve responses. "
        ) +"""
            Provide your result in the following JSON format:{"content": "your revised tweet"}.
            Remember, only respond with the JSON object in the specified format.
        """
        self.reflector_system_message = (
            f"You are an expert specialized in {topic}. " if topic else
            "You are an expert. "
        ) + (
            f"Your role is to be a {reflector_role}. " if reflector_role else
            "Your role is to provide constructive feedback. "
        ) + "Provide constructive feedback on the following response."
        
        self.evaluator_system_message = (
            f"You are an expert specialized in {topic}. " if topic else
            "You are an expert. "
        ) + (
            f"Your role is to be a {evaluator_role}. " if evaluator_role else
            "Your role is to assess responses. "
        ) + "Assess if the following response adequately addresses the given task."
        
        self.evaluation_parser = PydanticOutputParser(pydantic_object=Evaluation)
        self.generator_parser = PydanticOutputParser(pydantic_object=GeneratorOutput)
        
    def _generate_messages(self, task: str, previous_attempt: str = "", feedback: str = "") -> List[SystemMessage | HumanMessage]:
        messages = [
            SystemMessage(content=self.generator_system_message),
            HumanMessage(content=f"Task: {task}")
        ]
        if previous_attempt:
            messages.append(HumanMessage(content=f"Previous attempt: {previous_attempt}"))
        if feedback:
            messages.append(HumanMessage(content=f"Feedback: {feedback}"))
        messages.append(HumanMessage(content="Improved response:"))
        return messages

    def _reflect_messages(self, task: str, attempt: str) -> List[SystemMessage | HumanMessage]:
        return [
            SystemMessage(content=self.reflector_system_message),
            HumanMessage(content=f"Task: {task}\nResponse: {attempt}\nFeedback:")
        ]

    def _evaluate_messages(self, task: str, attempt: str) -> List[SystemMessage | HumanMessage]:
        return [
            SystemMessage(content=self.evaluator_system_message),
            HumanMessage(content=f"Task: {task}\nResponse: {attempt}"),
            HumanMessage(content="Evaluate the response and provide your assessment in the following JSON format:\n"
                                 '{\n'
                                 '    "is_good_enough": true_or_false,\n'
                                 '    "reasoning": "Your explanation for the evaluation"\n'
                                 '}')
        ]
        
    def _parse_generator_output(self, output: str) -> str:
        try:
            parsed = json.loads(output)
            if 'content' in parsed:
                return parsed['content']
        except json.JSONDecodeError:
            pass

        content_match = re.search(r'"content"\s*:\s*"(.*?)"', output, re.DOTALL)
        if content_match:
            return content_match.group(1)

        return output

    def run(self, task: dict) -> str:
        try:
            attempt = self.generator_llm.invoke(self._generate_messages(task))
            
            if isinstance(attempt, AIMessage):
                attempt = attempt.content

            attempt_content = self._parse_generator_output(attempt)

            for _ in range(self.max_iterations):
                evaluation_prompt = self._evaluate_messages(task, attempt_content)
                evaluation_result = self.evaluator_llm.invoke(evaluation_prompt)
                
                if isinstance(evaluation_result, AIMessage):
                    evaluation_result = evaluation_result.content

                try:
                    evaluation = self.evaluation_parser.parse(evaluation_result)
                except Exception:
                    logger.error("Failed to parse evaluation result", exc_info=True)
                    break
                
                if evaluation.is_good_enough:
                    return attempt_content
                
                feedback = self.reflector_llm.invoke(self._reflect_messages(task, attempt_content))
                attempt = self.generator_llm.invoke(self._generate_messages(task, attempt_content, feedback.content))
                
                if isinstance(attempt, AIMessage):
                    attempt = attempt.content

                attempt_content = self._parse_generator_output(attempt)
            
            return attempt_content  # Return the last attempt if max_iterations is reached
        except Exception as e:
            logger.error(f"An error occurred during reflection chain execution: {str(e)}", exc_info=True)
            return task.get('original_tweet', '')  # Return the original tweet if an error occurs
