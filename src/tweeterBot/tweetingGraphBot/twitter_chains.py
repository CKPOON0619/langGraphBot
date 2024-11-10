from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import langchain
from llm.ollamallm import  cool_ollama_llm, hot_ollama_llm, static_ollama_llm
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage

langchain.verbose = True

reflection_prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
      "Always provide detailed recommendations, including requests for length, virality and style. etc."
      "Only provide the critique and recommendations, do not include any other text. Inparticular, do not include any examples or tweets in your response."
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)



generation_prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a twitter techie influencer assistant tasked with writing exellent twitter posts"
      "Generate the best twitter post possible for the user's request."
      "If the user provides critique, respond with a revised version of your previous attempts"
      """
      Provide your result in the following JSON format:
        {{
            "content": "your revised tweet",
        }}    
      Remember, only respond with the JSON object in the specified format.
      """
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)

evaluation_prompt = ChatPromptTemplate.from_template("""
You are an expert social media consultant specializing in Twitter. Your task is to evaluate the quality of the following tweet and determine if it's good enough to be posted.

Tweet: {tweet}

Please consider the following criteria:
1. Clarity: Is the message clear and easy to understand?
2. Engagement: Is it likely to generate interest or interaction?
3. Relevance: Does it effectively convey the intended message?
4. Length: Is it within the appropriate length for a tweet?
5. Tone: Is the tone appropriate for the content and audience?

Provide your evaluation in the following JSON format:
{{
    "is_good_enough": true_or_false,
    "reasoning": "Your explanation for the evaluation"
}}

Remember, only respond with the JSON object in the specified format.
""")

class TweetEvaluation(BaseModel):
    is_good_enough: bool = Field(description="Whether the tweet is good enough to be posted")
    reasoning: str = Field(description="Explanation for the evaluation")
    
class TweetGeneration(BaseModel):
    content: str = Field(description="The generated or revised tweet")


def tweet_generation_to_ai_message(tweet_gen: TweetGeneration) -> AIMessage:
    return AIMessage(content=tweet_gen.content)


generation_parser = PydanticOutputParser(pydantic_object=TweetGeneration)
evaluation_parser = PydanticOutputParser(pydantic_object=TweetEvaluation)

generation_chain = generation_prompt | hot_ollama_llm | generation_parser | tweet_generation_to_ai_message
reflection_chain = reflection_prompt | cool_ollama_llm
evaluation_chain = evaluation_prompt | static_ollama_llm | evaluation_parser


