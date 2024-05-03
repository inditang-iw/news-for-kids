from openai import OpenAI
from headline import Headline

# create an instance of Headline
headline = Headline(api_key='1de03f53-a39f-4573-84b6-36a504d6d23a', section='uk-news')

# get article web url
article_web_url = headline.get_article_web_url()
print("webUrl: {}\n\n".format(article_web_url))
# get article text
article_text = headline.get_article_text()
print("Article text: {}\n\n".format(article_text))

# create a prompt for the OpenAI API
role_prompt = "You are a school teacher"
rewrite_prompt = "Rewrite the following article in a format suitable for kids aged 11-14 to read in 5 minutes: " + article_text

# call openai api to generate a summary of the article text
client = OpenAI(
    organization='org-6nwmJPLFhoVcsTHUI4tUAAGE',
    project='proj_oa45HVI0HZksNfOpJcaAFH4N',
    api_key='sk-proj-cpJ2hlLE3YFgAPr0ITFNT3BlbkFJwUPINQZjmJGijJMWrq9O'
)

# Call ChatGPT API to generate a summary of article_text
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": role_prompt},
        {"role": "user", "content": rewrite_prompt},
    ]
)
print(completion.choices[0].message.content)
