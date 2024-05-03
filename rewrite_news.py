""" This module provides functionality to rewrite news articles in a format suitable for kids """

from openai import OpenAI
from headline import Headline

class NewsRewriter:
    """
    This module provides functionality to rewrite news articles in a format suitable for kids aged 11-14 to read in 5 minutes.
    """

    def __init__(self, api_key, section):
        """
        Initializes the NewsRewriter object.

        Args:
            api_key (str): The API key for the Headline API.
            section (str): The section of the news to retrieve.

        Returns:
            None
        """
        self.headline = Headline(api_key=api_key, section=section)

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

    def rewrite_article_for_kids(self):
        """
        Rewrites the article in a format suitable for kids aged 11-14 to read in 5 minutes.

        Returns:
            str: The rewritten article.
        """
        article_text = self.get_article_text()
        role_prompt = "You are a school teacher"
        rewrite_prompt = "Rewrite the following article in a format suitable for kids aged 11-14 to read in 5 minutes: " + article_text

        client = OpenAI(
            organization='org-6nwmJPLFhoVcsTHUI4tUAAGE',
            project='proj_oa45HVI0HZksNfOpJcaAFH4N',
            api_key='sk-proj-cpJ2hlLE3YFgAPr0ITFNT3BlbkFJwUPINQZjmJGijJMWrq9O'
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": rewrite_prompt},
            ]
        )

        return completion.choices[0].message.content


# create an instance of NewsRewriter
news_rewriter = NewsRewriter(api_key='1de03f53-a39f-4573-84b6-36a504d6d23a', section='uk-news')

# get article web url
article_web_url = news_rewriter.get_article_web_url()
print(f"webUrl: {article_web_url}\n\n")

# get article text
original_article = news_rewriter.get_article_text()
print(f"Original article: {original_article}\n\n")

# rewrite the article for kids
rewritten_article = news_rewriter.rewrite_article_for_kids()
print(rewritten_article)
