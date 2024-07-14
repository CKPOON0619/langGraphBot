from langchain_huggingface import HuggingFaceEndpoint

hugging_llm = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03
)