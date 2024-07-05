from dotenv import load_dotenv
load_dotenv()


from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from chains import generation_chain, reflection_chain
from langgraph.graph import END, MessageGraph

REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: Sequence[BaseMessage]):
  # plug in the the state into messages placeholder to generate new message
  return generation_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    # Return reflection prompt message to the model so to improvise.
    res = reflection_chain.invoke({"messages": messages})
    # Check if res is a string or an object with content attribute
    content = res if isinstance(res, str) else getattr(res, 'content', str(res))
    return [HumanMessage(content=content)]

builder = MessageGraph()
builder.add_node(GENERATE,generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)


# Conditional edge
def should_continue(state: List[BaseMessage]):
  if len(state)>6:
    return END
  return REFLECT

builder.add_conditional_edges(GENERATE,should_continue)
builder.add_edge(REFLECT,GENERATE)
graph = builder.compile()

if __name__ == '__main__':
  print(graph.get_graph().draw_mermaid())
  print(graph.get_graph().print_ascii())
  inputs = HumanMessage(content="""
                        Make this tweet better: 
                        "
                          Thank you 
                          @RishiSunak
                          for your admirable leadership of the UK, and your active contribution to deepen the ties between India and the UK during your term in office. Best wishes to you and your family for the future.
                        "
                        """)
  response=graph.invoke(inputs)
  print(response)