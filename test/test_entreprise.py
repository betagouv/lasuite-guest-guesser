import pytest

from app.entreprise import Entreprise

@pytest.fixture()
def mock_lookup_via_api(monkeypatch):
    """
    Mock the _lookup_via_api method of the Entreprise class.
    """
    return_value = {
        "results": [
            {
                "nom_complet": "Test Company",
                "complements": {
                    "est_l100_3": True,
                    "est_service_public": False,
                    "collectivite_territoriale": None
                }
            }
        ]
    }
    monkeypatch.setattr('app.entreprise.Entreprise._lookup_via_api', lambda self: return_value)

@pytest.fixture()
def mock_lookup_locally(monkeypatch):
    """
    Mock the _lookup_locally method of the Entreprise class.
    """
    return_value = {
        "nom": "Test Company",
        "est_l100_3": True,
        "est_service_public": True,
        "nature_juridique": "1234",
        "collectivite_territoriale": True
    }
    monkeypatch.setattr('app.entreprise.Entreprise._lookup_locally', lambda self: return_value)
    

def test_entreprise_lookup_success(mock_lookup_via_api):
    entreprise = Entreprise("12345678901234")
    assert entreprise.siret == "12345678901234"
    assert entreprise.siren == "123456789"
    assert entreprise.nom == "Test Company"
    assert entreprise.l100_3 is True
    assert entreprise.service_public is False
    assert entreprise.collectivite_territoriale is False

def test_entreprise_lookup_fallback(monkeypatch, mock_lookup_locally):
    monkeypatch.setattr('app.entreprise.Entreprise._lookup_via_api', lambda self: ValueError("No results found"))
    entreprise = Entreprise("12345678901234")
    assert entreprise.siret == "12345678901234"
    assert entreprise.siren == "123456789"
    assert entreprise.nom == "Test Company"
    assert entreprise.l100_3 is True
    assert entreprise.service_public is True
    assert entreprise.collectivite_territoriale is True