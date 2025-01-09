from re import search

from agents.Search import tavily_search
from agents.AgentState import AgentState
from langgraph.graph import StateGraph, START, END

from agents.Research import call_search_tool,getResult


# Node 1 : Image Processing
# Node2 : LLM with tool (call model)
# Node3 : Search node
# Node4 : result node that is llm

## Router Function
def should_continue(state:  AgentState):
    message = state['search_results']
    if len(message) == 7:
        print("info : Reached maximum iteration 7 times")
        return "node3"
    last_message = message[-1]
    # If the LLM makes a tool call, then we route to the "action" node
    if last_message.tool_calls:
        return "node2"
    return "node3"


# define a new Graph

def run_graph(info, query):
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("node1", call_search_tool)
    workflow.add_node("node2", tavily_search)
    workflow.add_node("node3", getResult)

    # Set the entrypoint as `node1`
    # This means that this node is the first one called
    workflow.add_edge(START, "node1")

    workflow.add_edge('node2', 'node1')

    # We now add a conditional edge
    workflow.add_conditional_edges(
        "node1",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
    )
    workflow.add_edge("node3", END)

    agentGraph = workflow.compile()

    from langchain_core.messages import HumanMessage

    # Invoke the graph with initial state
    initial_state = {"info" : info, "query" : query, "search_results": []}

    result = agentGraph.invoke(initial_state)
    return result['search_results'][-1].content

# info = {"Date of birth" : "21-Nov-2007",
#         "Time of birth" : "10:00 AM",
#         "Location" : "Bhagalpur, Bihar, India",
#         "Name": "Prem",
#         "Sex": "Male"
# }
#
# query = "Generate horoscope from given info"
#
# response = run_graph(info, query)
# print(response)



