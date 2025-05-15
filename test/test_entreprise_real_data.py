import pytest

from app.entreprise import Entreprise

test_data = [
    # SIRET, service_public, l100_3, collectivite_territoriale
    ("21130055300016", True, True, True), # Ville de Marseille
    ("13002526500013", True, True, False), # DINUM
    ("059804062", True, False, False), # Régie des Transports Métropolitains
    ("130000805", True, False, False), # GIP Prevention Protection Judiciaire Jeunesse
    ("18310907300027", True, False, False), # GIP Inclusion
    ("54205118000066", False, False, False), # TotalEnergies
]

@pytest.mark.parametrize("siret,service_public,l100_3,collectivite_territoriale", test_data)
def test_with_real_siret(monkeypatch, siret, service_public, l100_3, collectivite_territoriale):
    """
    Test the Entreprise class with a real SIRET number. 
    In theory, the results should be the same whether the API is used or the local CSV file.
    """
    # Replace with a valid SIRET number for testing
    entreprise_api = Entreprise(siret)
    assert entreprise_api.service_public is service_public
    assert entreprise_api.l100_3 is l100_3
    assert entreprise_api.collectivite_territoriale is collectivite_territoriale

    # Turn off API access and test with local csv
    monkeypatch.setattr('app.entreprise.Entreprise._lookup_via_api', lambda self: ValueError("No results found"))
    entreprise_csv = Entreprise(siret)
    assert entreprise_csv.service_public == entreprise_api.service_public
    assert entreprise_csv.l100_3 == entreprise_api.l100_3
    assert entreprise_csv.collectivite_territoriale == entreprise_api.collectivite_territoriale