from langchain_community.chat_models import ChatOllama

# Initialize the ChatOllama model
ollama_llm = ChatOllama(
    model="llama3",  # Specify the model you want to use
    temperature=0.7     # Set the temperature parameter
)


# # Define a simple prompt to test the model
# prompt = "Tell me a joke about computers."

# # Send the prompt to the model and print the response
# response = ollama_llm.invoke(prompt)
# print(response)