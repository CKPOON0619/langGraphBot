import pytest
from unittest.mock import Mock, patch
from tweeterBot.tweetingChainBot.twitter_chain import TwitterReflectionChain
from langchain_core.messages import AIMessage

@pytest.fixture
def mock_llms():
    return Mock(), Mock(), Mock()

def test_twitter_reflection_chain_init(mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = TwitterReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    assert chain.generator_llm == generator_llm
    assert chain.reflector_llm == reflector_llm
    assert chain.evaluator_llm == evaluator_llm

def test_improve_tweet_success(mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = TwitterReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    
    with patch.object(chain, 'run', return_value="Improved tweet"):
        result = chain.improve_tweet("Original tweet")
    
    assert result == "Improved tweet"

def test_improve_tweet_ai_message(mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = TwitterReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    
    with patch.object(chain, 'run', return_value=AIMessage(content="Improved tweet")):
        result = chain.improve_tweet("Original tweet")
    
    assert result == "Improved tweet"

def test_improve_tweet_error(mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = TwitterReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    
    with patch.object(chain, 'run', side_effect=Exception("Test error")):
        result = chain.improve_tweet("Original tweet")
    
    assert result == "Original tweet"
