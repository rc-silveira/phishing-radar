import json
from ollama import ChatResponse, chat
from EmailInput import EmailInput
from fastapi import FastAPI

from AnalysisOutput import AnalysisOutput

app = FastAPI()


@app.post("/analysis")
async def analysis(email_input: EmailInput):
    response: ChatResponse = chat(
        model='llama3.2', messages=[
            {"role": "system",
             "content": "You are a phishing analyzer."
                        " Analyze the sender, subject, and body of the email and determine if it is phishing. "
                        "Respond only in JSON with the following fields: {is_a_threat: bool, explanation: str, signals: list[str], "
                        " official_email: str}. Do not write anything other than the JSON. If no official email exists, set to null. "
                        " Always respond in English."},
            {"role": "user", "content": f"{email_input.email}\n{email_input.subject}\n{email_input.body}\n"},
        ])
    ai_response = json.loads(response.message.content)
    return AnalysisOutput(**ai_response)
