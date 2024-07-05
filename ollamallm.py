from langchain_community.chat_models import ChatOllama

# Initialize the ChatOllama model
ollama_llm = ChatOllama(
    model="llama3",  # Specify the model you want to use
    format="json",    # Ensure the response format is JSON for proper function calling
    temperature=0.7     # Set the temperature parameter
)