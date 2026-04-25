import json

from ollama import ChatResponse, chat
from starlette.middleware.cors import CORSMiddleware

from EmailInput import EmailInput
from fastapi import FastAPI, HTTPException

from AnalysisOutput import AnalysisOutput

app = FastAPI()

origins = [
    "http://localhost:5173",
    "chrome-extension://pemkjkpcompkmpocoipmpgibpaedpfhd"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        ai_response = json.loads(response.message.content)
        return AnalysisOutput(**ai_response)
    except json.decoder.JSONDecodeError:
        print("You need to try again")
        raise HTTPException(status_code=500, detail="You need to try again")
