"""
This module provides a class for publishing articles to Medium using their API.
"""

import requests

class Medium:
    """
    A class used to represent the Medium platform.

    ...

    Attributes
    ----------
    api_key : str
        The API key used for authenticating with the Medium API.

    Methods
    -------
    publish_to_medium(data)
        Publishes an article to Medium.
    """
        
    def __init__(self, api_key):
        """
        Constructs all the necessary attributes for the Medium object.

        Parameters
        ----------
            api_key : str
                The API key used for authenticating with the Medium API.
        """
        self.api_key = api_key

        user_info = requests.get(f"https://api.medium.com/v1/me?accessToken={api_key}", timeout=5)
        user_json_info = user_info.json()
        print(f"user_json_info: {user_json_info}\n\n")

        self.medium_id = user_json_info['data']['id']

    def publish_to_medium(self, data):
        """
        Publishes an article to Medium.

        Parameters
        ----------
            data : dict
                A dictionary containing the article details. It should have the following keys:
                - "article_name": The title of the article.
                - "article_content": The content of the article.
                - "article_canonical_url": The canonical URL of the article.
        """
        token = self.api_key
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }
        print(f"header: {header}\n\n")

        article = {
            "title": data["article_name"],
            "contentFormat": "markdown",
            "content": data["article_content"],
            "canonicalUrl": data["article_canonical_url"],
            "tags": data["article_tags"].split(", "),
            "publishStatus": "public"
        }

        post_url = f"https://api.medium.com/v1/users/{self.medium_id}/posts"
        print(f"post_url: {post_url}\n\n")

        post_request = requests.post(url=post_url, headers=header, json=article, timeout=5)
        print(f"post_request: {post_request}\n\n")

        post_response_json_info = post_request.json()
        if post_request.status_code == requests.codes.created:
            return True
        
        print(f"post_response_json_info: {post_response_json_info}\n\n")
        return False

# Example usage
# medium_api_key = os.environ.get('MEDIUM_API_KEY')
# if medium_api_key is None:
#     print("Please set the MEDIUM_API_KEY environment variable.")
#     exit()
# medium = Medium(medium_api_key)
# article_data = {
#     "article_name": "My Article Title",
#     "article_content": "This is the content of my article.",
#     "article_canonical_url": "https://www.example.com",
#     "article_tags": "tag1, tag2, tag3"
# }
# if medium.publish_to_medium(article_data):
#     print("Article published successfully.")
# else:
#     print("Failed to publish article.")
