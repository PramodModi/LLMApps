from AgentState import GraphState
from LLM import llm
import re


def select_top_urls(state: GraphState) -> GraphState:
    """Based on the article synoses, choose the top-n articles to summarize."""
    news_query = state["news_query"]
    num_articles_tldr = state["num_articles_tldr"]

    # load all processed articles with full text but no summaries
    potential_articles = state["potential_articles"]

    # format the metadata
    formatted_metadata = "\n".join([f"{article['url']}\n{article['description']}\n" for article in potential_articles])

    prompt = f"""
    Based on the user news query:
    {news_query}

    Reply with a list of strings of up to {num_articles_tldr} relevant urls.
    Don't add any urls that are not relevant or aren't listed specifically.
    {formatted_metadata}
    """
    result = llm.invoke(prompt).content

    # use regex to extract the urls as a list
    url_pattern = r'(https?://[^\s",\)]+)'

    # Find all URLs in the text
    urls = re.findall(url_pattern, result)

    # add the selected article metadata to the state
    tldr_articles = [article for article in potential_articles if article['url'] in urls]

    # tldr_articles = [article for article in potential_articles if article['url'] in urls]
    state["tldr_articles"] = tldr_articles
    print("select_top_urls output = ",tldr_articles )

    return state