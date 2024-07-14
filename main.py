from dotenv import load_dotenv
load_dotenv()


from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from chains.twitter_chains import generation_chain, reflection_chain
from langgraph.graph import END, MessageGraph, MessagesState

REFLECT = "reflect"
GENERATE = "generate"   

def generation_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
  # plug in the the state into messages placeholder to generate new message
  print("\n\n\nGeneration node------") 
  for i,s in enumerate(state):
    print(i, "############################")
    print(s)

  response=generation_chain.invoke({"messages": state})
  print("\n---------------")
  print(response)
  return response


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
  # Return reflection prompt message to the model so to improvise.
  # res = reflection_chain.invoke({"messages": messages})
  print("\n\n\nReflection node------") 
  for i,s in enumerate(messages):
    print(i, "############################")
    print(s)
  response=reflection_chain.invoke({"messages": messages[:-1] + [HumanMessage(content=messages[-1].content)]})
  print("\n---------------")
  print(response)
  return [HumanMessage(content=response.content)]

builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

# Conditional edge
def should_continue(state: List[BaseMessage]):
  print("\n\n\nshould_continue ??????")
  for i,s in enumerate(state):
    print(i, "############################")
    print(s)
  if len(state) > 6:
    return END
  return REFLECT
builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()

print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

if __name__ == '__main__':
  inputs = HumanMessage(content="Make this tweet better: Thank you @RishiSunak for your admirable leadership of the UK, and your active contribution to deepen the ties between India and the UK during your term in office. Best wishes to you and your family for the future.")
  response=graph.invoke(inputs)
  print("--------result",response)