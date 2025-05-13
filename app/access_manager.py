from app.entreprise import Entreprise

class AccessManager:
    def __init__(self):
        pass

    def check_access(self, entreprise: Entreprise):
        raise NotImplementedError("This method should be implemented in a subclass.")
    

class LaSuiteAccessManager(AccessManager):
    """
    Class to manage access for La Suite.
    """
    def __init__(self):
        super().__init__()
        self.access_levels = {
            0: "external_guest",
            1: "greylist_guest",
            2: "public_agent"
        }


    def check_access(self, entreprise: Entreprise):
        """
        Compute access level for a given entreprise connecting to La Suite.
        """
        access_level = 0
        if entreprise.service_public:
            access_level += 1
        if entreprise.l100_3:
            access_level += 1
        if entreprise.collectivite_territoriale:
            access_level = 0
        return self.access_levels[access_level]