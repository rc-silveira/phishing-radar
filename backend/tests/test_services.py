from unittest.mock import MagicMock

import pytest

from backend.AnalysisOutput import AnalysisOutput
from backend.EmailInput import EmailInput
from backend.services import analyze_email


def test_analyze_email():
    ai_model = "llama-3.3-70b-versatile"
    llm_client = MagicMock()
    llm_client.client_communication.return_value = ('{"is_a_threat": true, "explanation": '
                                                    '"Suspicious email promoting products with urgency.",'
                                                    ' "signals": ["excessive dollar signs", "promotional language"], '
                                                    '"official_email": "contact@hsn.com"}')
    mocked_input = EmailInput(email="phyzhd@gmail.com", subject="Buy this Protein $$$$",
                              body="Condições da Promoção HSN. *Produtos Best Sellers Selecionados. "
                                   "*Válido em todas as marcas HSN exceto HSNaccessories e HSNpacks. "
                                   "*Não acumulável com outras promoções. *Evowhey Protein, Evowhey Protein Sem edulcorantes, "
                                   "Whey Protein Concentrate, Evolate 2.0, Evolate 2.0 Sem Edulcorantes")

    result = analyze_email(mocked_input, llm_client, ai_model)
    assert isinstance(result, AnalysisOutput)


def test_analyze_email_json_decode_error():
    ai_model = "llama-3.3-70b-versatile"
    llm_client = MagicMock()
    llm_client.client_communication.return_value = ('{"is_a_threat": true "explanation":  '
                                                    '"Suspicious email promoting products with urgency.",'
                                                    ' "signals": ["excessive dollar signs", "promotional language"], '
                                                    '"official_email": "contact@hsn.com"}')
    mocked_input = EmailInput(email="phyzhd@gmail.com", subject="Buy this Protein $$$$",
                              body="Condições da Promoção HSN. *Produtos Best Sellers Selecionados. "
                                   "*Válido em todas as marcas HSN exceto HSNaccessories e HSNpacks. "
                                   "*Não acumulável com outras promoções. *Evowhey Protein, Evowhey Protein Sem edulcorantes, "
                                   "Whey Protein Concentrate, Evolate 2.0, Evolate 2.0 Sem Edulcorantes")
    with pytest.raises(ValueError, match="LLM returned invalid JSON"):
        analyze_email(mocked_input, llm_client, ai_model)

def test_analyze_email_valdation_error():
    ai_model = "llama-3.3-70b-versatile"
    llm_client = MagicMock()
    llm_client.client_communication.return_value = ('{"is_a_threatttttt": true, "explanation":  '
                                                    '"Suspicious email promoting products with urgency.",'
                                                    ' "signals": ["excessive dollar signs", "promotional language"], '
                                                    '"official_email": "contact@hsn.com"}')
    mocked_input = EmailInput(email="phyzhd@gmail.com", subject="Buy this Protein $$$$",
                              body="Condições da Promoção HSN. *Produtos Best Sellers Selecionados. "
                                   "*Válido em todas as marcas HSN exceto HSNaccessories e HSNpacks. "
                                   "*Não acumulável com outras promoções. *Evowhey Protein, Evowhey Protein Sem edulcorantes, "
                                   "Whey Protein Concentrate, Evolate 2.0, Evolate 2.0 Sem Edulcorantes")
    with pytest.raises(ValueError, match="LLM response is missing or has invalid fields"):
        analyze_email(mocked_input, llm_client, ai_model)
