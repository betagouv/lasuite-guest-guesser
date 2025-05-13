from fastapi import FastAPI

from app.access_manager import LaSuiteAccessManager
from app.entreprise import Entreprise

api = FastAPI(title="La Suite Guest API",
    description="API to fetch company information using SIRET or SIREN number and figure out whether the user should be a guest with restricted access.",
    version="0.0.1",
)

@api.get("/")
def read_root():
    return {"message": "Welcome to the La Suite Guest API!"}

@api.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@api.get("/siret/{siret}")
def get_siret_info(siret: str):
    """
    Endpoint to fetch company information using SIRET or SIREN number.
    """
    entreprise = Entreprise(siret)
    return entreprise.to_dict()

@api.get("/access/{siret}")
def get_access_info(siret: str):
    """
    Endpoint to fetch access level for a given SIRET or SIREN number.
    """
    entreprise = Entreprise(siret)
    access_manager = LaSuiteAccessManager()
    access_level = access_manager.check_access(entreprise)
    return {"access_level": access_level}