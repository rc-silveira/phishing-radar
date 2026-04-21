from typing import Optional

from pydantic import BaseModel


class AnalysisOutput(BaseModel):
    is_a_threat: bool
    explanation: str
    signals: list[str]
    official_email: Optional[str]
