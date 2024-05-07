""" This module provides functionality to rewrite news articles in a format suitable for kids """

import os
from openai import OpenAI
from headline import Headline
from medium import Medium

class NewsRewriter:
    """
    This module provides functionality to rewrite news articles in a format suitable for kids aged
    11-14 to read in 5 minutes.
    """

    def __init__(self, news_api_key, section):
        """
        Initializes the NewsRewriter object.

        Args:
            news_api_key (str): The API key for the Headline API.
            section (str): The section of the news to retrieve.

        Returns:
            None
        """
        self.headline = Headline(api_key=news_api_key, section=section)

    def get_article_web_title(self):
        """
        Retrieves the web title of the article.

        Returns:
            str: The web title of the article.
        """
        return self.headline.get_article_web_title()

    def get_article_web_url(self):
        """
        Retrieves the web URL of the article.

        Returns:
            str: The web URL of the article.
        """
        return self.headline.get_article_web_url()

    def get_article_text(self):
        """
        Retrieves the text of the article.

        Returns:
            str: The text of the article.
        """
        return self.headline.get_article_text()

    def rewrite_article_for_kids(self, openai_api_key):
        """
        Rewrites the article in a format suitable for kids aged 11-14 to read in 5 minutes.

        Returns:
            str: The rewritten article.
        """
        article_text = self.get_article_text()
        role_prompt = "You are a school teacher"
        rewrite_prompt = "Rewrite the following article in a markdown format suitable for kids " + \
                         "aged 11-14 to read in 5 minutes and embed the link to the original " + \
                         "news article (" + self.get_article_web_url() + ") at the end: " \
                         + article_text

        client = OpenAI(
            organization='org-6nwmJPLFhoVcsTHUI4tUAAGE',
            project='proj_oa45HVI0HZksNfOpJcaAFH4N',
            api_key=openai_api_key
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": rewrite_prompt},
            ]
        )

        return completion.choices[0].message.content

# todo: refactor below as a function to receive 3 api keys as arguments
def rewrite_news(news_api_key, openai_api_key, medium_api_key):
    # create an instance of NewsRewriter
    news_rewriter = NewsRewriter(news_api_key=news_api_key, section='uk-news')
    
    # get article web title
    article_web_title = news_rewriter.get_article_web_title()
    print(f"webTitle: {article_web_title}\n\n")
    
    # get article web url
    article_web_url = news_rewriter.get_article_web_url()
    print(f"webUrl: {article_web_url}\n\n")
    
    # get article text
    original_article = news_rewriter.get_article_text()
    print(f"Original article: {original_article}\n\n")
    
    # rewrite the article for kids
    rewritten_article = news_rewriter.rewrite_article_for_kids(openai_api_key)
    print(rewritten_article)
    
    # publish the rewritten article to Medium
    medium = Medium(api_key=medium_api_key)
    article_data = {
        "article_name": article_web_title,
        # todo: ask openai to suggest a title
        "article_content": rewritten_article,
        "article_canonical_url": article_web_url,
        "article_tags": "kids, news, education"
        # todo: get tags from the article's pillar name & section name, or even ask openai to suggest tags
    }
    if medium.publish_to_medium(article_data):
        print("Article published successfully.")
    else:
        print("Failed to publish article.")

# todo: create a lambda handler function
# todo: retreive the api keys from ssm parameter store

# set api keys from environment variables
news_api_key = os.environ.get('NEWS_API_KEY')
if news_api_key is None:
    print("Please set the NEWS_API_KEY environment variable.")
    exit()

openai_api_key = os.environ.get('OPENAI_API_KEY')
if openai_api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

medium_api_key = os.environ.get('MEDIUM_API_KEY')
if medium_api_key is None:
    print("Please set the MEDIUM_API_KEY environment variable.")
    exit()

rewrite_news(news_api_key, openai_api_key, medium_api_key)
