import logging
import requests

from config import NATURE_JURIDIQUE_COLLECTIVITES

class Entreprise:
    """
    Class to fetch company information using SIRET or SIREN number.
    """
    def __init__(self, siret: str):
        self.nom = None
        self.siret = siret
        self.siren = siret[:9]
        self.collectivite_territoriale = None
        self.service_public = None
        self.l100_3 = None
        self.infos = self._fetch_infos()

    def _fetch_infos(self):
        try:
            infos = self._lookup_via_api()
            self.nom = infos.get("results")[0].get("nom_complet")
            self.l100_3 = infos.get("results")[0].get("complements").get("est_l100_3")
            self.service_public = infos.get("results")[0].get("complements").get("est_service_public")
            self.collectivite_territoriale = infos.get("results")[0].get("complements").get("collectivite_territoriale", False) is not None
        except Exception as e:
            logging.warning(f"API lookup failed: {e}")
            logging.info(f"Falling back to local lookup for SIRET: {self.siret}")
            infos = self._lookup_locally()
            print(infos)
            self.nom = infos.get("nom")
            self.l100_3 = infos.get("est_l100_3", False)
            self.service_public = infos.get("est_service_public", False)
            self.collectivite_territoriale = infos.get("collectivite_territoriale", False)
        return infos
    
    def _lookup_via_api(self):
        """
        Use Recherche entreprise to get information about the organization.
        """
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?q={self.siren}")
        r.raise_for_status()
        data = r.json()
        if not data.get("results"):
            raise ValueError("No results found")
        return r.json()
    
    def _lookup_locally(self):
        """
        Fallback to local lookup if API fails, so that we always reply.
        """
        with open("data/liste-administrations.csv", "r") as f:
            for line in f.readlines():
                if line.split(",")[0] == self.siren:
                    data = {
                        "est_service_public": True,
                        "nom": line.split(",")[1],
                        "est_l100_3": line.split(",")[3].strip("\n") == "True",
                        "nature_juridique": line.split(",")[2]
                    }
                    data["collectivite_territoriale"] = data["nature_juridique"] in NATURE_JURIDIQUE_COLLECTIVITES
                    return data
                
            return {
                "est_service_public": False,
                "nom": None,
                "est_l100_3": False,
                "nature_juridique": None,
                "collectivite_territoriale": False
            }