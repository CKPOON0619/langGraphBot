# Reflection Graph

from typing import List, Sequence, Callable, TypeVar
from enum import Enum
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph
from langchain.chains import LLMChain

T = TypeVar('T')

class NodeName(Enum):
    REFLECT = "REFLECT"
    GENERATE = "GENERATE"
    END = END

def create_generation_node(generation_chain: LLMChain) -> Callable[[Sequence[BaseMessage]], BaseMessage]:
    def generation_node(state: Sequence[BaseMessage]) -> BaseMessage:
        response = generation_chain.invoke({"messages": state})
        print("=========================================================\n")
        print("generation:", response.content)
        print("=========================================================\n")
        return response
    return generation_node

def create_reflection_node(reflection_chain: LLMChain) -> Callable[[Sequence[BaseMessage]], List[BaseMessage]]:
    def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
        response = reflection_chain.invoke({"messages": messages[:-1] + [HumanMessage(content=messages[-1].content)]})
        print("=========================================================\n")
        print("last message:\n", messages[-1].content)
        print("\nreflection:\n", response.content)
        print("=========================================================\n")
        return [HumanMessage(content=response.content)]
    return reflection_node

class ReflectionGraph:
    def __init__(self, 
                 generation_node: Callable[[Sequence[BaseMessage]], BaseMessage],
                 reflection_node: Callable[[Sequence[BaseMessage]], List[BaseMessage]],
                 evaluate_output: Callable[[str], NodeName],
                 max_iterations: int = 10):
        self.generation_node = generation_node
        self.reflection_node = reflection_node
        self.evaluate_output = evaluate_output
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.graph = self._build_graph()

    def _build_graph(self) -> MessageGraph:
        builder = MessageGraph()
        builder.add_node(NodeName.GENERATE.value, self.generation_node)
        builder.add_node(NodeName.REFLECT.value, self.reflection_node)
        builder.set_entry_point(NodeName.REFLECT.value)
        builder.add_conditional_edges(NodeName.GENERATE.value, self.should_continue)
        builder.add_edge(NodeName.REFLECT.value, NodeName.GENERATE.value)
        return builder.compile()

    def should_continue(self, state: List[BaseMessage]) -> str:
        self.current_iteration += 1
        print(f"Current iteration: {self.current_iteration}, Max iterations: {self.max_iterations}")
        
        if self.current_iteration >= self.max_iterations:
            return NodeName.END.value
        
        last_ai_message = next((msg for msg in reversed(state) if isinstance(msg, AIMessage)), None)
        if last_ai_message:
            try:
                evaluation = self.evaluate_output(last_ai_message.content)
                print("=========================================================\n")
                print("evaluation result:", evaluation)
                print("=========================================================\n")
                return evaluation.value
            except Exception as e:
                print(f"Error in evaluation: {e}")
                return NodeName.REFLECT.value
        return NodeName.REFLECT.value

    def invoke(self, input_message: HumanMessage) -> List[BaseMessage]:
        self.current_iteration = 0
        return self.graph.invoke(input_message)
