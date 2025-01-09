import os
from dotenv import load_dotenv, find_dotenv
from agents.AgentState import AgentState, getPrompt

_ = load_dotenv(find_dotenv())
mistral_api_key = os.environ["MISTRAL_API_KEY"]
tavily_api_key = os.environ["TAVILY_API_KEY"]

## Initialize Mistral model with search tool.
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    mistral_api_key=mistral_api_key,
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    # other params...
)

def callAstrologer(state:AgentState):

    template = """ You are an astrologer. Please reply the user query based on given info. 
                if you need additional information, please put in missing tag.
                You can refer previous data from search_result.
        info : {info}
        query : {query}
        search_results : {search_results}
        missing:

        """
    prompt = getPrompt(template, state)
    response = llm.invoke(prompt)
    state["search_results"].append(response)
    return state


info = {"Date of birth" : "21-Nov-2007",
        "Time of birth" : "10:00 AM",
        "Location" : "Bhagalpur, Bihar, India",
        "Name": "Prem",
        "Sex": "Male"
}
iniialState  = {"info" : info, "query" : "Generate horoscope from given info", "search_results": []}
response = callAstrologer(iniialState)
print(response)
