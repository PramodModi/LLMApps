# Import dot env and api keys
import os
from dotenv import load_dotenv, find_dotenv
from agents.AgentState import AgentState

_ = load_dotenv(find_dotenv())
mistral_api_key = os.environ["MISTRAL_API_KEY"]
tavily_api_key = os.environ["TAVILY_API_KEY"]


## Create a search tool
from langchain_community.tools.tavily_search import TavilySearchResults

online_search_tool = [TavilySearchResults(tavily_api_key = tavily_api_key, max_results=5)]

## Initialize Mistral model with search tool.
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    mistral_api_key=mistral_api_key,
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    # other params...
)
llm_with_tools = llm.bind_tools(online_search_tool)

# response = llm_with_tools.invoke("Tell me usage and side effect of Puse medicine")
# print(response)

from langchain_core.prompts import ChatPromptTemplate

def getPrompt(template, state):
    chat_prompt_template = ChatPromptTemplate.from_template(template)
    context = state["search_results"]
    query = state["query"]
    return chat_prompt_template.invoke({"context": context, "query": query})

def call_search_tool(state:AgentState):
    template = """
        reply to query with given context. Create search query for each individual items separately in a list.
        {context}
        {query}
    """
    prompt = getPrompt(template, state)
    response = llm_with_tools.invoke(prompt)
    state["search_results"].append(response)
    return state

def getResult(state:AgentState):

    template = """ You are summarization assistant. Summarize the given context in section wise.
        Use the tabular format wherever it is possible. Answer the given query if there is any.
        {context}
        {query}

        """
    prompt = getPrompt(template, state)
    response = llm.invoke(prompt)
    state["search_results"].append(response)
    return state

