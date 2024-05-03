from theguardian import theguardian_content

class Headline:
    def __init__(self, api_key, section):
        content = theguardian_content.Content(api=api_key, section=section)
        json_content = content.get_content_response()
        first_api_url = json_content['response']['results'][0]['apiUrl']
        article_content = theguardian_content.Content(api=api_key, url=first_api_url, **{"show-blocks": "all"})
        self.json_article_content = article_content.get_content_response()

    def get_article_web_url(self):
        return self.json_article_content['response']['content']['webUrl']

    def get_article_text(self):
        return self.json_article_content['response']['content']['blocks']['body'][0]['bodyTextSummary']

