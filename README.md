# news-for-kids
A Gen AI based application to rewrite headline news into a format suitable for kids to read

## Prerequisites
- The Guardian's API Key - https://open-platform.theguardian.com/
- theguardian-api-python - https://github.com/prabhath6/theguardian-api-python
- OpenAI API Key - https://platform.openai.com/docs/api-reference/chat
- Medium API Reference - https://github.com/Medium/medium-api-docs?tab=readme-ov-file#33-posts

## Ideas on other features
1. Store API keys in AWS Systems Manager Parameter Store (not Secrets Manager as it is not free)
2. Scheduled runs using AWS Lambda & CloudWatch events
3. CI/CD pipeline and tests