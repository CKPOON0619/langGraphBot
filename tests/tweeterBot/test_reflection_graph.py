from unittest.mock import Mock
from langchain_core.messages import HumanMessage, AIMessage
from tweeterBot.graphs.reflection_graph import ReflectionGraph, NodeName, create_generation_node, create_reflection_node

def test_create_generation_node():
    mock_chain = Mock()
    mock_chain.invoke.return_value = AIMessage(content="Generated content")
    node = create_generation_node(mock_chain)
    result = node([HumanMessage(content="Input")])
    assert isinstance(result, AIMessage)
    assert result.content == "Generated content"

def test_create_reflection_node():
    mock_chain = Mock()
    mock_chain.invoke.return_value = AIMessage(content="Reflection")
    node = create_reflection_node(mock_chain)
    result = node([HumanMessage(content="Input"), AIMessage(content="Output")])
    assert isinstance(result[0], HumanMessage)
    assert result[0].content == "Reflection"

def test_reflection_graph():
    mock_generation = Mock(side_effect=[
        AIMessage(content="Generated 1"),
        AIMessage(content="Generated 2")
    ])
    mock_reflection = Mock(side_effect=[
        [HumanMessage(content="Reflected 1")],
        [HumanMessage(content="Reflected 2")]
    ])
    mock_evaluate = Mock(side_effect=[NodeName.REFLECT, NodeName.END])

    graph = ReflectionGraph(
        generation_node=mock_generation,
        reflection_node=mock_reflection,
        evaluate_output=mock_evaluate,
        max_iterations=2
    )

    result = graph.invoke(HumanMessage(content="Initial"))

    assert len(result) == 5  # Initial + 2 * (generation + reflection)
    assert result[0].content == "Initial"
    assert result[1].content == "Reflected 1"
    assert result[2].content == "Generated 1"
    assert result[3].content == "Reflected 2"
    assert result[4].content == "Generated 2"

    assert mock_generation.call_count == 2
    assert mock_reflection.call_count == 2
    assert mock_evaluate.call_count == 1

def test_reflection_graph_max_iterations():
    mock_generation = Mock(side_effect=[
        AIMessage(content="Generated 1"),
        AIMessage(content="Generated 2"),
        AIMessage(content="Generated 3")
    ])
    mock_reflection = Mock(side_effect=[
        [HumanMessage(content="Reflected 1")],
        [HumanMessage(content="Reflected 2")],
        [HumanMessage(content="Reflected 3")]
    ])
    mock_evaluate = Mock(return_value=NodeName.REFLECT)

    graph = ReflectionGraph(
        generation_node=mock_generation,
        reflection_node=mock_reflection,
        evaluate_output=mock_evaluate,
        max_iterations=3
    )

    result = graph.invoke(HumanMessage(content="Initial"))

    assert len(result) == 7  # Initial + 3 * (generation + reflection)
    assert result[0].content == "Initial"
    assert result[1].content == "Reflected 1"
    assert result[2].content == "Generated 1"
    assert result[3].content == "Reflected 2"
    assert result[4].content == "Generated 2"
    assert result[5].content == "Reflected 3"
    assert result[6].content == "Generated 3"

    assert mock_generation.call_count == 3
    assert mock_reflection.call_count == 3
    assert mock_evaluate.call_count == 2
