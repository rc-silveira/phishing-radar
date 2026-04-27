import json, os

import requests
from starlette.middleware.cors import CORSMiddleware

from EmailInput import EmailInput
from fastapi import FastAPI, HTTPException, Header

from AnalysisOutput import AnalysisOutput
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "chrome-extension://pemkjkpcompkmpocoipmpgibpaedpfhd"
]
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analysis")
async def analysis(email_input: EmailInput, x_token: str = Header(None)):
    valid_token = requests.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={x_token}")
    if valid_token.status_code != 200:
        raise HTTPException(status_code=valid_token.status_code, detail="Invalid API key")

    else:

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": "You are a phishing analyzer."
                            " Analyze the sender, subject, and body of the email and determine if it is phishing. "
                            "Respond only in JSON with the following fields: {is_a_threat: bool, explanation: str, signals: list[str], "
                            " official_email: str}. Do not write anything other than the JSON. If no official email exists, set to null. "
                            " Always respond in English."},
                {"role": "user", "content": f"{email_input.email}\n{email_input.subject}\n{email_input.body}\n"},
            ],
            model="llama-3.3-70b-versatile")
        try:
            ai_response = json.loads(chat_completion.choices[0].message.content)
            return AnalysisOutput(**ai_response)
        except json.decoder.JSONDecodeError:
            print("You need to try again")
            raise HTTPException(status_code=500, detail="You need to try again")
