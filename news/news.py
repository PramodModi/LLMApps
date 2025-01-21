
# Ref : https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/news_tldr_langgraph.ipynb
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

news_api_key = os.environ["NEWS_API_KEY"]
from newsapi import NewsApiClient

from pydantic import BaseModel, Field

newsapi = NewsApiClient(news_api_key)

query = 'ai news of the day'

all_articles = newsapi.get_everything(q=query,
                                      sources='google-news,bbc-news,techcrunch',
                                      domains='techcrunch.com, bbc.co.uk',
                                      language='en',
                                      sort_by='relevancy',)


all_articles['articles'][0]


class NewsApiParams(BaseModel):
    q: str = Field(description="1-3 concise keyword search terms that are not too specific")
    #sources: str =Field(description="comma-separated list of sources from: 'abc-news,associated-press,bbc-news,bbc-sport,bloomberg,business-insider,cbc-news,cbs-news,cnn,financial-post,fortune'")
    sources:str=Field(description="comma-separated list of sources from: 'google-news-in, the-hindu,the-times-of-india, bloomberg,business-insider,cbc-news,financial-post,fortune,abc-news,associated-press,bbc-news' ")
    from_param: str = Field(description="date in format 'YYYY-MM-DD' Two days ago minimum. Extend up to 30 days on second and subsequent requests.")
    to: str = Field(description="date in format 'YYYY-MM-DD' today's date unless specified")
    language: str = Field(description="language of articles 'en' unless specified one of ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh']")
    sort_by: str = Field(description="sort by 'relevancy', 'popularity', or 'publishedAt'")









