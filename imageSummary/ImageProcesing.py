## Boiler plat code start

# Import dot env and api keys
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
mistral_api_key = os.environ["MISTRAL_API_KEY"]


## Initialize Mistral model with Pixel.
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    mistral_api_key=mistral_api_key,
   # model="mistral-large-latest",
    model="pixtral-12b-2409",
    temperature=0,
    max_retries=2,
    max_tokens = 1024
    # other params...
)

## Boiler plat code end

# Reduce the size of Image, otherwise token is out of context size
from PIL import Image
def reduceImageSize(imageFile, tempPath):
    img = Image.open(imageFile)
    img.thumbnail((812, 812))  # Adjust the size as needed
    img.save(tempPath)

# Encode image
import base64
import os

def encode_image(image_path, tempPath):
    """Getting the base64 string"""
    reduceImageSize(image_path, tempPath)
    with open(tempPath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


## Generate response from LLM

from langchain_core.messages import HumanMessage

def image_summarize(img_base64, prompt):
    """Make image summary"""

    msg = llm.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ]
            )
        ]
    )
    return msg.content

## Generate Prompt

def run_llm(image_path, query):
    template = """You are an expert to read and summerize the image. 
     Please give a small and crisp summary of image first. Then, Reply the query ask by user. 
     Do not add items name if it is not available or not clear to you in response. 
     Provide data in tabular format wherever it is possible. Please use Indian Rupees if there is any amount or cost.
     At the end you should provide the ou should provide the summary of image in details.
     
    {query}
    """
    tempPath = "./data/temp.jpg"
    base64_image = encode_image(image_path, tempPath)
    #query = "Let me know the price of each items in Indian rupees."
    prompt = template.format(query=query)
    result = image_summarize(base64_image, prompt)
    return result

