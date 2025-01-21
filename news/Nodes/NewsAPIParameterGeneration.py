from AgentState import GraphState
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from datetime import datetime, timedelta

from LLM import llm
from news import NewsApiParams


def generate_newsapi_params(state: GraphState) -> GraphState:
    """Based on the query, generate News API params."""
    # initialize parser to define the structure of the response
    parser = JsonOutputParser(pydantic_object=NewsApiParams)

    # retrieve today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Calculate from_date
    from_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

    # retrieve list of past search params
    past_searches = state["past_searches"]

    # retrieve number of searches remaining
    num_searches_remaining = state["num_searches_remaining"]

    # retrieve the user's query
    news_query = state["news_query"]

    template = """
    Today is {today_date}.
    From date is {from_date}

    Create a param dict for the News API based on the user query:
    {query}

    These searches have already been made. Loosen the search terms to get more results.
    {past_searches}

    Following these formatting instructions:
    {format_instructions}

    Including this one, you have {num_searches_remaining} searches remaining.
    If this is your last search, use all news sources and a 30 days search range.
    """

    # create a prompt template to merge the query, today's date, and the format instructions
    # prompt_template = PromptTemplate(
    #     template=template,
    #     input_variables= {
    #         "today": today_date, "query": news_query, "past_searches": past_searches,
    #                "num_searches_remaining": num_searches_remaining},
    #     partial_variables={"format_instructions": parser.get_format_instructions()}
    # )

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["today_date", "from_date", "query", "past_searches", "num_searches_remaining"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # create prompt chain template
    chain = prompt_template | llm | parser

    # invoke the chain with the news api query
    result = chain.invoke({"query": news_query, "today_date": today_date, "from_date":from_date, "past_searches": past_searches,
                           "num_searches_remaining": num_searches_remaining})
    print("generate_newsapi_params result = ", result)

    # update the state
    state["newsapi_params"] = result

    return state
