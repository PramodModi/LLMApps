import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
mistral_api_key = os.environ["MISTRAL_API_KEY"]

from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    mistral_api_key=mistral_api_key,
    # model="mistral-large-latest",
    model="pixtral-12b-2409",
    temperature=0,
    max_retries=2,
    max_tokens=1024
    # other params...
)