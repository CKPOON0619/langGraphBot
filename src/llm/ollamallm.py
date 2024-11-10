from langchain_community.chat_models import ChatOllama

# Initialize the ChatOllama model
ollama_llm = ChatOllama(
    model="llama3",  # Specify the model you want to use
    temperature=0.7     # Set the temperature parameter
)

hot_ollama_llm = ChatOllama(
    model="llama3",  # Specify the model you want to use
    temperature=1     # Set the temperature parameter
)

cool_ollama_llm = ChatOllama(
    model="llama3",  # Specify the model you want to use
    temperature=0.3     # Set the temperature parameter
)

static_ollama_llm = ChatOllama(
    model="llama3",  # Specify the model you want to use
    temperature=0     # Set the temperature parameter
)
