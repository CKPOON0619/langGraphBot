import pytest
from unittest.mock import Mock, patch
from tweeterBot.chains.reflection_chain import ReflectionChain
from langchain_core.messages import AIMessage

@pytest.fixture
def mock_llms():
    return Mock(), Mock(), Mock()

def test_reflection_chain_init(mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = ReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    assert chain.generator_llm == generator_llm
    assert chain.reflector_llm == reflector_llm
    assert chain.evaluator_llm == evaluator_llm

def test_generate_messages():
    chain = ReflectionChain(Mock(), Mock(), Mock())
    messages = chain._generate_messages("Task", "Previous", "Feedback")
    assert len(messages) == 5
    assert messages[0].content == chain.generator_system_message
    assert "Task: Task" in messages[1].content
    assert "Previous attempt: Previous" in messages[2].content
    assert "Feedback: Feedback" in messages[3].content
    assert messages[4].content == "Improved response:"

def test_reflect_messages():
    chain = ReflectionChain(Mock(), Mock(), Mock())
    messages = chain._reflect_messages("Task", "Attempt")
    assert len(messages) == 2
    assert messages[0].content == chain.reflector_system_message
    assert "Task: Task" in messages[1].content
    assert "Response: Attempt" in messages[1].content

def test_evaluate_messages():
    chain = ReflectionChain(Mock(), Mock(), Mock())
    messages = chain._evaluate_messages("Task", "Attempt")
    assert len(messages) == 3
    assert messages[0].content == chain.evaluator_system_message
    assert "Task: Task" in messages[1].content
    assert "Response: Attempt" in messages[1].content
    assert "JSON format" in messages[2].content

def test_parse_generator_output_json():
    chain = ReflectionChain(Mock(), Mock(), Mock())
    output = '{"content": "Parsed content"}'
    result = chain._parse_generator_output(output)
    assert result == "Parsed content"

def test_parse_generator_output_regex():
    chain = ReflectionChain(Mock(), Mock(), Mock())
    output = 'Some text "content": "Parsed content" more text'
    result = chain._parse_generator_output(output)
    assert result == "Parsed content"

def test_parse_generator_output_fallback():
    chain = ReflectionChain(Mock(), Mock(), Mock())
    output = "Unparseable content"
    result = chain._parse_generator_output(output)
    assert result == "Unparseable content"

@patch('tweeterBot.chains.reflection_chain.logger')
def test_run_success(mock_logger, mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = ReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    
    generator_llm.invoke.return_value = AIMessage(content='{"content": "Generated"}')
    evaluator_llm.invoke.return_value = AIMessage(content='{"is_good_enough": true, "reasoning": "Good"}')
    
    result = chain.run({"original_tweet": "Original"})
    assert result == "Generated"

@patch('tweeterBot.chains.reflection_chain.logger')
def test_run_max_iterations(mock_logger, mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = ReflectionChain(generator_llm, reflector_llm, evaluator_llm, max_iterations=2)
    
    generator_llm.invoke.return_value = AIMessage(content='{"content": "Generated"}')
    evaluator_llm.invoke.return_value = AIMessage(content='{"is_good_enough": false, "reasoning": "Not good"}')
    reflector_llm.invoke.return_value = AIMessage(content="Feedback")
    
    result = chain.run({"original_tweet": "Original"})
    assert result == "Generated"
    assert generator_llm.invoke.call_count == 3  # Initial + 2 iterations

@patch('tweeterBot.chains.reflection_chain.logger')
def test_run_error(mock_logger, mock_llms):
    generator_llm, reflector_llm, evaluator_llm = mock_llms
    chain = ReflectionChain(generator_llm, reflector_llm, evaluator_llm)
    
    generator_llm.invoke.side_effect = Exception("Test error")
    
    result = chain.run({"original_tweet": "Original"})
    assert result == "Original"
    mock_logger.error.assert_called()
