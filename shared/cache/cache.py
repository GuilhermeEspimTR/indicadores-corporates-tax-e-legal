import os
from shared.requests import Requests
from requests import Response
import csv
import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
from io import StringIO

class Cache(Requests):
    
    file_name: str = "cache"
    __extension: str = ".csv"
    __current_path: str = f"{os.path.dirname(__file__)}/files/"
    
    
    def __init__(self) -> None:
        pass
    
    
    def get_from_azure_devops(self, url: str) -> pd.DataFrame:
        
        PATH: str = f"{self.__current_path}{self.file_name}{self.__extension}"
        
        if not self.__exists():   
            RESPONSE: Response = self.run(url)
            
            if RESPONSE:     
                work_items: list = RESPONSE.json().get('value', [])  
                 
                with open(PATH, "w", encoding='utf-8') as file:   
                    WRITER = csv.DictWriter(file, fieldnames=work_items[0].keys())                    
                    WRITER.writeheader()
                    
                    for row in work_items:
                        WRITER.writerow(row)
                    
                    file.close()
        
        return pd.read_csv(PATH)
    
    
    # def get_from_sharepoint(self, url: str, file_url: str, email: str, password: str) -> None:
    #     PATH: str = f"{self.__current_path}{self.file_name}{self.__extension}"
    #     if not self.__exists():
    #         auth_context = AuthenticationContext(url)
    #         auth_context.acquire_token_for_user(email, password)
    #         ctx = ClientContext(url, auth_context)

    #         # Baixar o arquivo
    #         response = File.open_binary(ctx, file_url)
    #         csv_content = response.content.decode('utf-8')
    #         csv_io = StringIO(csv_content)
    
    def get_from_sharepoint(self) -> None:
        PATH: str = f"{self.__current_path}{self.file_name}{self.__extension}"
        return pd.read_csv(PATH) 
            
    
    
    def __exists(self) -> bool:
        PATH: str = f"{self.__current_path}{self.file_name}{self.__extension}"
        return os.path.exists(PATH)