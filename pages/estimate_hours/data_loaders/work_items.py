from shared.cache.cache import Cache
from pandas import DataFrame
import pandas as pd
import ast

class WorkItems(Cache):
    
    url: str = "https://analytics.dev.azure.com/tr-ggo/_odata/v1.0/WorkItems?$select=WorkItemId, WorkItemType, Title, State, TagNames, OriginalEstimate&$expand=AssignedTo($select=UserName), CreatedOn($select=Date)&$filter=(Project/ProjectName eq 'ONVIO BR' AND ChangedOn/Date gt 2024-11-27T13:27:05.036Z AND State eq 'Active')&$orderby=Title asc"
    data: DataFrame = DataFrame()
    
    def __init__(self) -> None:
        self.auth = ("", "03P7OWMfefonGg9jRYK6cbElYT5VpfykfYUaMYNcbcni9u6ZgRczJQQJ99BDACAAAAADXeeUAAASAZDO3Adz")
        self.file_name = "work_items"
        self.data = self.get_from_azure_devops(self.url)
        
        self.data['UserName'] = self.data['AssignedTo'].apply(self.extract_user_name)
        
        self.data['CreatedOn'] = self.data['CreatedOn'].apply(self.extract_date)
        self.data['CreatedOn'] = pd.to_datetime(self.data['CreatedOn'], errors='coerce')
        self.data = self.data.rename(columns={'CreatedOn': 'CreatedDate'})
        
        self.data = self.data.sort_values(by=['UserName', 'CreatedDate'])
        
        
    def extract_user_name(self, val):
        if pd.isna(val) or val == '':
            return None
        if isinstance(val, dict):
            return val.get('UserName')
        if isinstance(val, str) and val.startswith('{'):
            try:
                return ast.literal_eval(val).get('UserName')
            except Exception:
                return None
        return None
    
    def extract_date(self, val):
        if pd.isna(val) or val == '':
            return None
        if isinstance(val, dict):
            return val.get('Date')
        if isinstance(val, str) and val.startswith('{'):
            try:
                return ast.literal_eval(val).get('Date')
            except Exception:
                return None
        return val
    
    