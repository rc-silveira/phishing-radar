import os

from starlette.middleware.cors import CORSMiddleware

from backend.EmailInput import EmailInput
from fastapi import FastAPI, HTTPException, Header

from groq import Groq
from dotenv import load_dotenv

from backend.adapters.GroqAdapter import GroqAdapter
from backend.auth import get_auth_token
from backend.services import analyze_email

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "chrome-extension://pemkjkpcompkmpocoipmpgibpaedpfhd"
]
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
adapter = GroqAdapter(client)
model = os.environ.get("AI_MODEL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analysis")
async def analysis(email_input: EmailInput, x_token: str = Header(None)):
    auth_token = get_auth_token(x_token)
    if auth_token:
        try:
            ai_response = analyze_email(email_input,adapter, model)
            return ai_response
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException( status_code=401, detail="Invalid Token")
