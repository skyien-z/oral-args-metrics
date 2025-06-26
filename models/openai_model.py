from models import BaseModel


class OpenAIModel(BaseModel):
    def __init__(self, api_key: str):
        from openai import AzureOpenAI
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint="https://api-ai-sandbox.princeton.edu/",
            api_version="2024-02-01"
        )

    def generate(self, messages: str, greedy_generation: bool) -> str:
        if greedy_generation:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                temperature=0.0,
                max_tokens=100,
                top_p=1.0,
                messages=messages
            )
        else:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
        return response.choices[0].message.content
