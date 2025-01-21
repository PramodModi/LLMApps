from langgraph.graph import Graph, END

from AgentState import GraphState
from Nodes.NewsAPIParameterGeneration import generate_newsapi_params
from Nodes.ResultFormatter import format_results
from Nodes.RetrieveArticlesMetadata import retrieve_articles_metadata
from Nodes.RetrieveArticlesText import retrieve_articles_text
from Nodes.SelectTopUrls import select_top_urls
from Nodes.Summarize_Articles import summarize_articles


def articles_text_decision(state: GraphState) -> str:
    """Check results of retrieve_articles_text to determine next step."""
    print("num_searches_remaining = ", state["num_searches_remaining"])
    if state["num_searches_remaining"] == 0:
        # if no articles with text were found return END
        if len(state["potential_articles"]) == 0:
            state["formatted_results"] = "No articles with text found."
            return "END"
        # if some articles were found, move on to selecting the top urls
        else:
            return "select_top_urls"
    else:
        # if the number of articles found is less than the number of articles to summarize, continue searching
        if len(state["potential_articles"]) < state["num_articles_tldr"]:
            return "generate_newsapi_params"
        # otherwise move on to selecting the top urls
        else:
            return "select_top_urls"


workflow = Graph()

workflow.set_entry_point("generate_newsapi_params")

workflow.add_node("generate_newsapi_params", generate_newsapi_params)
workflow.add_node("retrieve_articles_metadata", retrieve_articles_metadata)
workflow.add_node("retrieve_articles_text", retrieve_articles_text)
workflow.add_node("select_top_urls", select_top_urls)
workflow.add_node("summarize_articles", summarize_articles)
workflow.add_node("format_results", format_results)
# workflow.add_node("add_commentary", add_commentary)

workflow.add_edge("generate_newsapi_params", "retrieve_articles_metadata")
workflow.add_edge("retrieve_articles_metadata", "retrieve_articles_text")
# # if the number of articles with parseable text is less than number requested, then search for more articles
workflow.add_conditional_edges(
    "retrieve_articles_text",
    articles_text_decision,
    {
        "generate_newsapi_params": "generate_newsapi_params",
        "select_top_urls": "select_top_urls",
        "END": END
    }
    )
workflow.add_edge("select_top_urls", "summarize_articles")
workflow.add_conditional_edges(
    "summarize_articles",
    lambda state: "format_results" if len(state["tldr_articles"]) > 0 else "END",
    {
        "format_results": "format_results",
        "END": END
    }
    )
workflow.add_edge("format_results", END)

app = workflow.compile()

def run_workflow_query_search(query: str, num_searches_remaining: int = 7, num_articles_tldr: int = 4):
    """Run the LangGraph workflow and display results."""
    initial_state = {
        "news_query": query,
        "num_searches_remaining": num_searches_remaining,
        "newsapi_params": {},
        "past_searches": [],
        "articles_metadata": [],
        "scraped_urls": [],
        "num_articles_tldr": num_articles_tldr,
        "potential_articles": [],
        "tldr_articles": [],
        "formatted_results": "No articles with text found."
    }
    try:
        result = app.invoke(initial_state)

        return result["formatted_results"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

#
# query = "news on Artificial agent in India"
# num_articles_tldr = 4
# result1 = run_workflow_query_search(query, num_articles_tldr=num_articles_tldr)
# print(result1)