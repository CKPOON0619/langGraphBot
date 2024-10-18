from dotenv import load_dotenv
load_dotenv()

from langchain_core.exceptions import OutputParserException
from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from tweetingBot.twitter_chains import generation_chain, reflection_chain, evaluation_chain, TweetEvaluation
from langgraph.graph import END, MessageGraph

REFLECT = "reflect"
GENERATE = "generate"   
EVALUATE = "evaluate"
def generation_node(state: Sequence[BaseMessage]) -> BaseMessage:
  # invoke generation chain to generate a new message
  response=generation_chain.invoke({"messages": state})
  print("=========================================================\n")
  print("generation:", response.content)
  print("=========================================================\n")
  return response


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
  # invoke reflection with the last message returned by generation node as the human message 
  # to futher prompt generation node for improvement
  response=reflection_chain.invoke({"messages": messages[:-1] + [HumanMessage(content=messages[-1].content)]})
  # return only the response as a new human message, prompt the model to improve the tweet
  print("=========================================================\n")
  print("last message:\n", messages[-1].content)
  print("\nreflection:\n", response.content)
  print("=========================================================\n")
  return [HumanMessage(content=response.content)]


builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(REFLECT)

# Conditional edge
def should_continue(state: List[BaseMessage]):
  if len(state) > 10:  # Increased max iterations
    return END
  
  # All reflection response are pretended to be human message, so the last AI message is the last tweet generated
  last_ai_message = next((msg for msg in reversed(state) if isinstance(msg, AIMessage)), None)
  if last_ai_message:
    try:
        evaluation: TweetEvaluation = evaluation_chain.invoke({"tweet": last_ai_message.content})
        print("=========================================================\n")
        print("evaluation:\n", evaluation)
        print("=========================================================\n")
        if evaluation.is_good_enough:
            return END
        print("continue......")
    except OutputParserException as e:
        print(f"Error parsing output: {e}")
        # You can decide how to handle parsing errors, e.g., continue or end
        return REFLECT 
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()

print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

if __name__ == '__main__':
  inputs = HumanMessage(content="Make this tweet better: Thank you @RishiSunak for your admirable leadership of the UK, and your active contribution to deepen the ties between India and the UK during your term in office. Best wishes to you and your family for the future.")
  response = graph.invoke(inputs)
  final_tweet = next(msg for msg in reversed(response) if msg.type == "ai")
  print("--------result:\n", final_tweet.content)