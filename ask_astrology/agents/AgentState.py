from typing import TypedDict


# Define the state schema
class AgentState(TypedDict):
    info: dict
    query: str
    search_results: list

from langchain_core.prompts import ChatPromptTemplate
def getPrompt(template, state):
    chat_prompt_template = ChatPromptTemplate.from_template(template)
    info = state["info"]
    query = state["query"]
    search_results = state["search_results"]
    return chat_prompt_template.invoke({"info": info, "query": query, "search_results" : search_results})