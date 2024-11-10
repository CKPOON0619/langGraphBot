
from typing import List
from langchain_core.messages import BaseMessage, HumanMessage
from .twitter_chains import generation_chain, reflection_chain, evaluation_chain
from ..graphs.reflection_graph import ReflectionGraph, create_generation_node, create_reflection_node, NodeName


def evaluate_tweet(tweet: str) -> NodeName:
    evaluation = evaluation_chain.invoke({"tweet": tweet})
    print("=========================================================\n")
    print("evaluation:\n", evaluation)
    print("=========================================================\n")
    if evaluation.is_good_enough:
        return NodeName.END
    return NodeName.REFLECT

generation_node = create_generation_node(generation_chain)
reflection_node = create_reflection_node(reflection_chain)

reflection_graph = ReflectionGraph(
    generation_node=generation_node,
    reflection_node=reflection_node,
    evaluate_output=evaluate_tweet
)

def improve_tweet(tweet: str, graph: ReflectionGraph) -> str:
    inputs = HumanMessage(content=f"Make this tweet better: {tweet}")
    response: List[BaseMessage] = graph.invoke(inputs)
    final_tweet = next(msg.content for msg in reversed(response) if msg.type == "ai")
    return final_tweet


if __name__ == '__main__':
  original_tweet = "Thank you @RishiSunak for your admirable leadership of the UK, and your active contribution to deepen the ties between India and the UK during your term in office. Best wishes to you and your family for the future."
  improved_tweet = improve_tweet(original_tweet,reflection_graph)
  print("Original tweet:", original_tweet)
  print("Improved tweet:", improved_tweet)
