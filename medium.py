import requests

def publish_to_medium(data):
    token = "2830f8007464c48cc654d4bc1ad2ad46b55115433b81b3da5f95384f3602d7796"
    header = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8'
    }
    print(f"header: {header}\n\n")
    
    user_info = requests.get(f"https://api.medium.com/v1/me?accessToken={token}")
    user_json_info = user_info.json()
    print(f"user_json_info: {user_json_info}\n\n")

    article = {
        "title": data["article_name"],
        "contentFormat": "markdown",
        "content": data["article_content"],
        "canonicalUrl": data["article_canonical_url"],
        "tags": data["article_tags"].split(", "),
        "publishStatus": "draft"
    }

    post_url = f"https://api.medium.com/v1/users/{user_json_info['data']['id']}/posts"
    print(f"post_url: {post_url}\n\n")

    post_request = requests.post(url = post_url, headers = header, json = article)
    print(f"post_request: {post_request}\n\n")

    post_response_json_info = post_request.json()
    if post_request.status_code == requests.codes.created:
        return True
    else:
        print(f"post_response_json_info: {post_response_json_info}\n\n")
        return False
    
article_data = {
    "article_name": "My Article Title",
    "article_content": "This is the content of my article.",
    "article_canonical_url": "https://www.example.com",
    "article_tags": "tag1, tag2, tag3"
}

if publish_to_medium(article_data):
    print("Article published successfully.")
else:
    print("Failed to publish article.")