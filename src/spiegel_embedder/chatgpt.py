import openai


class chatgpt_api:

    def __init__(self, api_key):
        openai.api_key = api_key

    def embed(self, text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        return embeddings
