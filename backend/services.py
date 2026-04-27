import json

from pydantic import ValidationError

from backend.AnalysisOutput import AnalysisOutput
from backend.EmailInput import EmailInput
from backend.llm_client import LlmClient


def analyze_email(email_input: EmailInput, llm_client: LlmClient, ai_model: str) -> AnalysisOutput:
    message = [
        {"role": "system",
         "content": "You are a phishing analyzer."
                    " Analyze the sender, subject, and body of the email and determine if it is phishing. "
                    "Respond only in JSON with the following fields: {is_a_threat: bool, explanation: str, signals: list[str], "
                    " official_email: str}. Do not write anything other than the JSON. If no official email exists, set to null. "
                    " Always respond in English."},
        {"role": "user", "content": f"{email_input.email}\n{email_input.subject}\n{email_input.body}\n"},
    ]
    ai_client_response = llm_client.client_communication(message, ai_model)
    try:
        ai_output = json.loads(ai_client_response)
        return AnalysisOutput(**ai_output)
    except json.decoder.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
    except ValidationError:
        raise ValueError("LLM response is missing or has invalid fields")