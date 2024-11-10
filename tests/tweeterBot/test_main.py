from unittest.mock import patch, Mock

from tweeterBot.tweetingGraphBot.main import evaluate_tweet, improve_tweet, NodeName
from langchain_core.messages import AIMessage, HumanMessage

def test_evaluate_tweet():
    tweet = "This is a test tweet"
    result = evaluate_tweet(tweet)
    assert isinstance(result, NodeName)
    assert result in [NodeName.END, NodeName.REFLECT]

@patch('tweeterBot.tweetingGraphBot.main.evaluation_chain')
def test_evaluate_tweet_with_mock(mock_evaluation_chain):
    mock_evaluation_chain.invoke.return_value = Mock(
        is_good_enough=True,
        reasoning="Good tweet"
    )
    
    tweet = "This is a test tweet"
    result = evaluate_tweet(tweet)
    
    assert result == NodeName.END
    mock_evaluation_chain.invoke.assert_called_once_with({"tweet": tweet})

@patch('tweeterBot.tweetingGraphBot.main.ReflectionGraph')
def test_improve_tweet_with_mock(mock_reflection_graph):
    mock_graph_instance = mock_reflection_graph.return_value
    mock_graph_instance.invoke.return_value = [
        HumanMessage(content="Make this tweet better: This is a test tweet"),
        AIMessage(content="This is an improved test tweet")
    ]
    
    tweet = "This is a test tweet"
    result = improve_tweet(tweet, mock_graph_instance)
    
    assert result == "This is an improved test tweet"
    mock_graph_instance.invoke.assert_called_once()

def test_node_name_enum():
    assert NodeName.END.value == "__end__"
    assert NodeName.REFLECT.value == "REFLECT"
    assert NodeName.GENERATE.value == "GENERATE"
    assert len(NodeName) == 3  # Ensure there are only two enum values

# You can add more tests here as needed
