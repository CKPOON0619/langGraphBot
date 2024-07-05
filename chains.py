from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI()

# from huggingfacellm import hugging_llm
# llm = hugging_llm

from ollamallm import ollama_llm
llm=ollama_llm


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
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)


generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm