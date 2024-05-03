""" This module contains the Headline class, which represents a news headline article. """

from theguardian import theguardian_content

class Headline:
    """
    A class representing a headline article.

    Attributes:
        api_key (str): The API key for accessing The Guardian API.
        section (str): The section of the news to retrieve headlines from.
        json_article_content (dict): The JSON response containing the article content.

    Methods:
        get_article_web_url: Returns the web URL of the article.
        get_article_text: Returns the text summary of the article.
    """

    def __init__(self, api_key, section):
        """
        Initializes a Headline object.

        Args:
            api_key (str): The API key for accessing The Guardian API.
            section (str): The section of the news to retrieve headlines from.
        """
        content = theguardian_content.Content(api=api_key, section=section)
        json_content = content.get_content_response()
        first_api_url = json_content['response']['results'][0]['apiUrl']
        article_content = theguardian_content.Content(api=api_key, url=first_api_url, **{"show-blocks": "all"})
        self.json_article_content = article_content.get_content_response()

    def get_article_web_url(self):
        """
        Returns the web URL of the article.

        Returns:
            str: The web URL of the article.
        """
        return self.json_article_content['response']['content']['webUrl']

    def get_article_text(self):
        """
        Returns the text summary of the article.

        Returns:
            str: The text summary of the article.
        """
        return self.json_article_content['response']['content']['blocks']['body'][0]['bodyTextSummary']
    