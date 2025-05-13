import logging
import requests

from config import NATURE_JURIDIQUE_COLLECTIVITES, RECHERCHE_ENTREPRISE_API_BASE_URL

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
        self.source = None
        self.infos = self._fetch_infos()

    def __repr__(self):
        return f"""Entreprise(
        nom={self.nom},
        siret={self.siret},
        service_public={self.service_public},
        l100_3={self.l100_3},
        collectivite_territoriale={self.collectivite_territoriale}
) source: {self.source}
"""
    def to_dict(self):
        return {
            "nom": self.nom,
            "siret": self.siret,
            "siren": self.siren,
            "service_public": self.service_public,
            "l100_3": self.l100_3,
            "collectivite_territoriale": self.collectivite_territoriale,
            "source": self.source
        }

    def _fetch_infos(self):
        try:
            infos = self._lookup_via_api()
            self.nom = infos.get("results")[0].get("nom_complet")
            self.l100_3 = infos.get("results")[0].get("complements").get("est_l100_3")
            self.service_public = infos.get("results")[0].get("complements").get("est_service_public")
            self.collectivite_territoriale = infos.get("results")[0].get("complements").get("collectivite_territoriale", False) is not None
            self.source = "API Recherche Entreprise"
        except Exception as e:
            logging.warning(f"API lookup failed: {e}")
            logging.info(f"Falling back to local lookup for SIRET: {self.siret}")
            infos = self._lookup_locally()
            self.nom = infos.get("nom")
            self.l100_3 = infos.get("est_l100_3", False)
            self.service_public = infos.get("est_service_public", False)
            self.collectivite_territoriale = infos.get("collectivite_territoriale", False)
            self.source = "Local CSV"
        return infos
    
    def _lookup_via_api(self):
        """
        Use Recherche entreprise to get information about the organization.
        """
        r = requests.get(f"{RECHERCHE_ENTREPRISE_API_BASE_URL}/search?q={self.siren}")
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
                    return self.parse_csv_line(line)
                
            return {
                "est_service_public": False,
                "nom": None,
                "est_l100_3": False,
                "nature_juridique": None,
                "collectivite_territoriale": False
            }

    @staticmethod
    def parse_csv_line(line):
        data = {
            "est_service_public": True,
            "nom": line.split(",")[1],
            "est_l100_3": line.split(",")[3].strip("\n") == "True",
            "nature_juridique": line.split(",")[2]
        }
        data["collectivite_territoriale"] = data["nature_juridique"] in NATURE_JURIDIQUE_COLLECTIVITES
        return data