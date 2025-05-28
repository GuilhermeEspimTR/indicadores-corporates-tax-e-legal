from shared.cache.cache import Cache
from pandas import DataFrame

class LoggedHours(Cache):
    
    def __init__(self) -> None:
        self.file_name = "logged_hours"
        self.data = self.get_from_sharepoint()
        self.data = self.data[self.data["projectName"] == "ONVIO BR"]