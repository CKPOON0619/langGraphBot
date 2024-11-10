from langchain.llms import BaseLLM
from ..chains.reflection_chain import ReflectionChain
from typing import Dict, Any
from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)

class TwitterReflectionChain(ReflectionChain):
    def __init__(self, 
                 generator_llm: BaseLLM, 
                 reflector_llm: BaseLLM, 
                 evaluator_llm: BaseLLM, 
                 max_iterations: int = 5):
        super().__init__(
            generator_llm=generator_llm,
            reflector_llm=reflector_llm,
            evaluator_llm=evaluator_llm,
            max_iterations=max_iterations,
            generator_role="viral Twitter influencer",
            reflector_role="social media strategist",
            evaluator_role="Twitter engagement expert",
            topic="Twitter content creation"
        )

    def improve_tweet(self, original_tweet: str) -> str:
        try:
            task = {"original_tweet": original_tweet}
            result = self.run(task)
            
            if isinstance(result, AIMessage):
                result = result.content
            
            return result
        except Exception as e:
            logger.error(f"An error occurred while improving the tweet: {str(e)}", exc_info=True)
            return original_tweet  # Return the original tweet if an error occurs

    # Optional: override the run method if you need Twitter-specific behavior
    # def run(self, task: str) -> str:
    #     # Twitter-specific implementation
    #     return super().run(task)
