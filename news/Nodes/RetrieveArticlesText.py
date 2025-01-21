from AgentState import GraphState


import requests
from bs4 import BeautifulSoup

def retrieve_articles_text(state: GraphState) -> GraphState:
    """Web scrapes to retrieve article text."""
    # load retrieved article metadata
    articles_metadata = state["articles_metadata"]
    # Add headers to simulate a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    # create list to store valid article dicts
    potential_articles = []

    # iterate over the urls
    for article in articles_metadata:
        # extract the url
        url = article['url']

        # use beautiful soup to extract the article content
        response = requests.get(url, headers=headers)

        # check if the request was successful
        if response.status_code == 200:
            # parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # find the article content
            text = soup.get_text(strip=True)

            # append article dict to list
            potential_articles.append(
                {"title": article["title"], "url": url, "description": article["description"], "text": text})

            # append the url to the processed urls
            state["scraped_urls"].append(url)

    print("retrieve_articles_text output = ", potential_articles)
    # append the processed articles to the state
    state["potential_articles"].extend(potential_articles)

    return state