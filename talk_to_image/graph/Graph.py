from re import search

from agents import ImageProcessing
from agents import Research
from agents import Search
from agents.AgentState import AgentState
from langgraph.graph import StateGraph, START, END

from agents.Research import call_search_tool


# Node 1 : Image Processing
# Node2 : LLM with tool (call model)
# Node3 : Search node
# Node4 : result node that is llm

## Router Function
def should_continue(state:  AgentState):
    message = state['search_results']
    last_message = message[-1]
    # If the LLM makes a tool call, then we route to the "action" node
    if last_message.tool_calls:
        return "node3"
    return "node4"


# define a new Graph

def getChat_to_image(image_path, query):
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("node1", ImageProcessing.getImageSummary)
    workflow.add_node("node2", call_search_tool)
    workflow.add_node("node3", Search.tavily_search)
    workflow.add_node("node4", Research.getResult)

    # Set the entrypoint as `node1`
    # This means that this node is the first one called
    workflow.add_edge(START, "node1")

    workflow.add_edge('node1', 'node2')

    # We now add a conditional edge
    workflow.add_conditional_edges(
        "node2",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
    )
    workflow.add_edge("node3", "node4")
    workflow.add_edge("node4", END)

    agentGraph = workflow.compile()

    from langchain_core.messages import HumanMessage

    # Invoke the graph with initial state
    initial_state = {"image_path": image_path, "query": query, "search_results": []}

    result = agentGraph.invoke(initial_state)
    return result['search_results'][-1].content

# image_path = "../data/medicine.jpg"
# query = "let me know medicines usage and side effects"
# response = getChat_to_image(image_path, query)
# print(response)



