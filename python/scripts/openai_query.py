import openai


class OpenAIQuery:
    def __init__(self, client: openai.OpenAI):
        self._client = client

    def query(self, context: str, query: str) -> str:
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. \
                            You answer the question based on the context provided. \
                            The context might look fragmented, but you can make it more readable by parsing the context and summarizing it.",
                },
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"},
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content
