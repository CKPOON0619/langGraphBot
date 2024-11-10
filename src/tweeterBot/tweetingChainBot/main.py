from llm.ollamallm import cool_ollama_llm,static_ollama_llm,hot_ollama_llm
from ..tweetingChainBot.twitter_chain import TwitterReflectionChain

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    generator_llm = hot_ollama_llm # Higher temperature for creative generation
    reflector_llm = cool_ollama_llm # Lower temperature for structured reflection
    evaluator_llm = static_ollama_llm  # Even lower temperature for consistent evaluation

    twitter_chain = TwitterReflectionChain(
        generator_llm=generator_llm,
        reflector_llm=reflector_llm,
        evaluator_llm=evaluator_llm
    )

    original_tweet = "Thank you @RishiSunak for your admirable leadership of the UK, and your active contribution to deepen the ties between India and the UK during your term in office. Best wishes to you and your family for the future."
    
    try:
        improved_tweet = twitter_chain.improve_tweet(original_tweet)
        print("Original tweet:", original_tweet)
        print("Improved tweet:", improved_tweet)
    except Exception as e:
        logger.exception("An error occurred during tweet improvement")
        if hasattr(e, 'errors'):
            for error in e.errors():
                print(f"Error detail: {error}")

if __name__ == '__main__':
    main()
