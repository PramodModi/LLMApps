# Import dot env and api keys
import os
from dotenv import load_dotenv, find_dotenv

from agents.AgentState import AgentState

_ = load_dotenv(find_dotenv())
mistral_api_key = os.environ["MISTRAL_API_KEY"]
tavily_api_key = os.environ["TAVILY_API_KEY"]


## Create a search tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage

#online_search_tool = [TavilySearchResults(tavily_api_key = tavily_api_key, max_results=5)]
def tavily_search(state:AgentState):
    all_search_result = {}
    # Create an instance of the TavilySearchResults tool
    tool = TavilySearchResults(max_results=5, search_depth="advanced", include_answer=True, tavily_api_key = tavily_api_key)

    # Perform the search using the query from the state
    message = state['search_results']
    tool_invocation = message[-1].tool_calls
    print("tool_invocation = ", tool_invocation)
    for q in tool_invocation:
        query = q['args']
        print("query = ", query)
        # Invoke tool
        result = tool.invoke(query)
        all_search_result[query["query"]] = result

    # Extract relevant information from the search results
    state["search_results"].append(all_search_result)  # Assuming 'results' contains the search results
    return state
