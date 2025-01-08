from typing import TypedDict


# Define the state schema
class AgentState(TypedDict):
    image_path: str
    query: str
    search_results: list
