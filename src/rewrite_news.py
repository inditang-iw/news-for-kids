""" This module provides functionality to rewrite news articles in a format suitable for kids """

import boto3
import random
from openai import OpenAI
from headline import Headline
from medium import Medium

GUARDIAN_API_KEY_PARAM = '/news-for-kids/guardian-api-key'
OPENAI_API_KEY_PARAM = '/news-for-kids/openai-api-key'
MEDIUM_API_KEY_PARAM = '/news-for-kids/medium-api-key'
OPENAI_ORGANIZATION_PARAM = '/news-for-kids/openai-organization'
OPENAI_PROJECT_PARAM = '/news-for-kids/openai-project'
NEWS_SECTIONS = [
    'uk-news', 
    'sport', 
    'music', 
    'world', 
    'football', 
    'food', 
    'books', 
    'lifeandstyle', 
    'environment', 
    'technology', 
    'tv-and-radio'
]

class NewsRewriter:
    """
    This module provides functionality to rewrite news articles in a format suitable for kids aged
    10-12 to read in 5 minutes.
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

    def rewrite_article_for_kids(self, openai_api_key, openai_organization, openai_project):
        """
        Rewrites the article in a format suitable for kids aged 10-12 to read in 5 minutes.

        Returns:
            str: The rewritten article.
        """
        article_text = self.get_article_text()
        role_prompt = "You are a school teacher"
        rewrite_prompt = "Rewrite the following article in a markdown format suitable for kids " + \
                         "aged 10-12 to read in 5 minutes and embed the link to the original " + \
                         "news article (" + self.get_article_web_url() + ") at the end: " \
                         + article_text

        client = OpenAI(
            organization=openai_organization,
            project=openai_project,
            api_key=openai_api_key
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": rewrite_prompt},
            ],
            timeout=50,
        )

        return completion.choices[0].message.content

def rewrite_news(news_api_key, openai_api_key, medium_api_key, openai_organization, openai_project):
    """
    Rewrites a news article for kids using the NewsRewriter class and publishes it to Medium.

    Args:
        news_api_key (str): The API key for accessing the news API.
        openai_api_key (str): The API key for accessing the OpenAI API.
        medium_api_key (str): The API key for accessing the Medium API.

    Returns:
        None
    """
    # randomly choose a section 
    section = random.choice(NEWS_SECTIONS)

    # create an instance of NewsRewriter
    news_rewriter = NewsRewriter(news_api_key=news_api_key, section=section)

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
    rewritten_article = news_rewriter.rewrite_article_for_kids(openai_api_key, openai_organization, openai_project)
    print(rewritten_article)

    # publish the rewritten article to Medium
    medium = Medium(api_key=medium_api_key)
    article_data = {
        "article_name": article_web_title,
        # todo: ask openai to suggest a title
        "article_content": rewritten_article,
        "article_canonical_url": article_web_url,
        "article_tags": "kids, news, education"
        # todo: get tags from the article's pillar name & section name,
        # or even ask openai to suggest tags
    }
    if medium.publish_to_medium(article_data):
        print("Article published successfully.")
    else:
        print("Failed to publish article.")

def retrieve_params():
    """
    Retrieves API keys from AWS SSM Parameter Store.

    Returns:
        dict: A dictionary containing the retrieved API keys.
    """
    ssm = boto3.client('ssm')
    response = ssm.get_parameters(
        Names=[
            GUARDIAN_API_KEY_PARAM, 
            OPENAI_API_KEY_PARAM, 
            MEDIUM_API_KEY_PARAM,
            OPENAI_ORGANIZATION_PARAM,
            OPENAI_PROJECT_PARAM
        ],
        WithDecryption=True
    )
    params = {}
    for parameter in response['Parameters']:
        params[parameter['Name']] = parameter['Value']
    return params

# pylint: disable=unused-argument
def lambda_handler(event, context):
    """
    Handles the Lambda function invocation.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The context object passed to the Lambda function.

    Returns:
        dict: A dictionary containing a message.

    """
    # todo: retreive the api keys from ssm parameter store
    params = retrieve_params()
    rewrite_news(
        params[GUARDIAN_API_KEY_PARAM],
        params[OPENAI_API_KEY_PARAM],
        params[MEDIUM_API_KEY_PARAM],
        params[OPENAI_ORGANIZATION_PARAM],
        params[OPENAI_PROJECT_PARAM]
        )
    # todo: invoke the rewrite_news function with the api keys
    return {
        'message' : 'return link to the medium article here?'
    }

# the code below is for local testing
lambda_handler(None, None)
