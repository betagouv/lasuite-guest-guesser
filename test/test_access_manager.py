import pytest

from app.access_manager import LaSuiteAccessManager
from app.entreprise import Entreprise

lsam = LaSuiteAccessManager()

@pytest.mark.parametrize("service_public,l100_3,collectivite_territoriale,expected_access_level", [
    (True, True, False, "public_agent"),
    (True, False, False, "greylist_guest"),
    (False, True, False, "greylist_guest"), # should this even be possible?
    (False, False, False, "external_guest"),
    (False, False, True, "external_guest"), # This shouldn't be possible, but let's test it
    (True, True, True, "external_guest"), # Collectivités are guests
])
def test_check_access(monkeypatch, service_public, l100_3, collectivite_territoriale, expected_access_level):
    """
    Test the check_access method of LaSuiteAccessManager.
    """
    # Mock the Entreprise class to return specific values
    monkeypatch.setattr('app.entreprise.Entreprise._fetch_infos', lambda self: None)
    entreprise = Entreprise("12345678901234")
    entreprise.service_public = service_public
    entreprise.l100_3 = l100_3
    entreprise.collectivite_territoriale = collectivite_territoriale 

    # Check access level
    access_level = lsam.check_access(entreprise)
    assert access_level == expected_access_level
