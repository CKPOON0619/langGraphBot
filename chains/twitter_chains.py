from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import langchain
from llm.ollamallm import ollama_llm

llm=ollama_llm
langchain.verbose = True

reflection_prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
      "Always provide detailed recommendations, including requests for length, virality and style. etc."
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)



generation_prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a twitter techie influencer assistant tasked with writing exellent twitter posts"
      "Generate the best twitter post possible for the user's request."
      "If the user provides critique, respond with a revised version of your previous attempts."
      "Include ONLY the tweet content in your response without anything else as if you are writing the tweet directly. "
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)


generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm




# def display_formatted_prompt(prompt_template, input_data):
#     formatted_prompt = prompt_template.format_messages(**input_data)
#     print("----------------------------------------")
#     print("Formatted Prompt:")
#     for message in formatted_prompt:
#         print(f"{message.type}: {message.content}")
#     print("\n")
#     return formatted_prompt
# # Test the generation chain
# input_data = {"messages": [{"role": "user", "content": "Write a tweet about AI."}]}

# generation_response = generation_chain.invoke(input_data)
# display_formatted_prompt(generation_prompt,input_data)
# print("Generation Response:====================")
# print(generation_response.content)

# # Test the reflection chain
# display_formatted_prompt(reflection_prompt, {"messages": [{"role": "user", "content": generation_response.content}]})
# reflection_response = reflection_chain.invoke({"messages": [{"role": "user", "content": generation_response.content}]})
# print("Reflection Response:=====================")
# print(reflection_response.content)
