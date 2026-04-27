from backend.llm_client import LlmClient

class GroqAdapter(LlmClient):
    def __init__(self, client):
        self.client = client

    def client_communication(self, message:list [str], model: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=message,
            model=model
        )
        return chat_completion.choices[0].message.content