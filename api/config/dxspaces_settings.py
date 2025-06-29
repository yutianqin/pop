# api\config\dxspaces_settings.py
from pydantic_settings import BaseSettings

try:
    from dxspaces import DXSpacesClient

    have_staging = True
except Exception:
    have_staging = False


class RegistrationTest:
    def __init__(self, reg_list):
        self.reg_list = reg_list

    def __getitem__(self, key):
        if self.reg_list == "all":
            return True
        elif self.reg_list == "none":
            return False
        elif key in self.reg_list.replace(" ", "").split(","):
            return True
        return False


class Settings(BaseSettings):
    dxspaces_enabled: bool = False
    dxspaces_url: str = "http://localhost:8001"
    dxspaces_registration: str = ""

    @property
    def dxspaces(self):
        if have_staging:
            return DXSpacesClient(self.dxspaces_url, debug=True)
        else:
            return None

    @property
    def registration_methods(self):
        if have_staging:
            return RegistrationTest(self.dxspaces_registration)
        else:
            return RegistrationTest("none")

    model_config = {"env_file": ".env", "extra": "allow"}


dxspaces_settings = Settings()
