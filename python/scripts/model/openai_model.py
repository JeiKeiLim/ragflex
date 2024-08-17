"""This module contains the OpenAIModel class, which is a subclass of ModelManager.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

import os

from openai import OpenAI

from scripts.model.model import ModelManager


class OpenAIModel(ModelManager):
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.5,
        prompt: str = "You are a helpful assistant.",
    ) -> None:
        super().__init__()
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not set")

        self._client = OpenAI(api_key=openai_key)

        self.__model_name = model_name
        self.__temperature = temperature
        self.__prompt = prompt

    def _query(self, context: str, query: str) -> str:
        response = self._client.chat.completions.create(
            model=self.__model_name,
            messages=[
                {
                    "role": "system",
                    "content": self.__prompt,
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuery: {query}"
                },
            ],
            temperature=self.__temperature,
        )

        return response.choices[0].message.content
