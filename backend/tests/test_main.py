from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.AnalysisOutput import AnalysisOutput
from backend.main import app

client = TestClient(app)
auth_token = "123456789xpto"


def test_analysis():
    with patch("backend.main.get_auth_token", return_value=True):
        with patch("backend.main.analyze_email",
                   return_value=AnalysisOutput(is_a_threat=True, explanation="...", signals=[], official_email=None)):
            response = client.post("/analysis",
                                   headers={"x-token": f"{auth_token}"},
                                   json= {"email": "phyzhd@gmail.com", "subject": "Buy this Protein $$$$",
                                          "body": "Condições da Promoção HSN."})
        assert response.status_code == 200

def test_analyze_401_Unauthorized():
    with patch("backend.main.get_auth_token", return_value=False):
        with patch("backend.main.analyze_email",
                   return_value=AnalysisOutput(is_a_threat=True, explanation="...", signals=[], official_email=None)):
            response = client.post("/analysis",
                                   headers={"x-token": f"{auth_token}"},
                                   json={"email": "phyzhd@gmail.com", "subject": "Buy this Protein $$$$",
                                         "body": "Condições da Promoção HSN."})
        assert response.status_code == 401

def test_analyze_400_BadRequest():
    with patch("backend.main.get_auth_token", return_value=True):
        with patch("backend.main.analyze_email",
                   side_effect=ValueError("Bad Request")):
            response = client.post("/analysis",
                                   headers={},
                                   json={"email": "phyzhd@gmail.com", "subject": "Buy this Protein $$$$",
                                         "body": "Condições da Promoção HSN."})
        assert response.status_code == 400