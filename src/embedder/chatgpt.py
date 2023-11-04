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

    def get_response(self, prompt):
        # Generate a response
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2024,
            n=1,
            stop=None,
            temperature=0.3,
        )

        response = completion.choices[0].text
        return response
