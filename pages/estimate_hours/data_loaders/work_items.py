from shared.cache.cache import Cache
from pandas import DataFrame
import pandas as pd
import ast
import asyncio

class WorkItems(Cache):
    
    url: str = ("https://analytics.dev.azure.com/tr-ggo/_odata/v1.0/WorkItems?"
                "$select=WorkItemId,Title,State,OriginalEstimate,WorkItemType"
                "&$expand=Iteration($select=IterationPath),"
                "AssignedTo($select=UserName),"
                "Links("
                    "$select=TargetWorkItem;"
                    "$filter=("
                        "TargetWorkItem/Project/ProjectName eq 'ONVIO BR' "
                        "AND TargetWorkItem/ChangedOn/Date gt 2024-11-28T17:17:51.739Z "
                        "AND TargetWorkItem/State eq 'Active' "
                        "AND TargetWorkItem/WorkItemType eq 'Task'"
                    ");"
                    "$expand=TargetWorkItem("
                        "$select=WorkItemId,WorkItemType,Title,State,TagNames,OriginalEstimate,CreatedOn;"
                        "$expand=AssignedTo($select=UserName),CreatedOn($select=Date),Iteration($select=IterationPath)"
                    ")"
                ")"
                "&$filter=("
                    "Project/ProjectName eq 'ONVIO BR' "
                    "AND ChangedOn/Date gt 2024-11-28T17:28:14.856Z "
                    "AND State eq 'Active' "
                    "AND WorkItemType eq 'User Story'"
                ")"
                "&$orderby=Title asc,WorkItemId asc")
    
    data: DataFrame = DataFrame()
    
    
    def __init__(self) -> None:
        self.auth = ("", "03P7OWMfefonGg9jRYK6cbElYT5VpfykfYUaMYNcbcni9u6ZgRczJQQJ99BDACAAAAADXeeUAAASAZDO3Adz")
        self.file_name = "work_items"
        self.data = self.get_from_azure_devops(self.url)
        
        self.data["UserName"] = self.data["AssignedTo"].apply(self.extract_user_name)
        self.data["IterationPath"] = self.data["Iteration"].apply(self.extract_iteration_path)
        
    
    def refresh(self) -> None:
        self.delete_cache()
        self.data = self.get_from_azure_devops(self.url)
            
    
    def extract_user_name(self, val):
        if pd.isna(val) or val == "":
            return None
        if isinstance(val, dict):
            return val.get("UserName")
        if isinstance(val, str) and val.startswith("{"):
            try:
                return ast.literal_eval(val).get("UserName")
            except Exception:
                return None
        return None
    
    def extract_iteration_path(self, val):
        if pd.isna(val) or val == "":
            return None
        if isinstance(val, dict):
            return val.get("IterationPath")
        if isinstance(val, str) and val.startswith("{"):
            try:
                return ast.literal_eval(val).get("IterationPath")
            except Exception:
                return None
        return None
    
    
    def extract_tasks(self, links) -> list:
        tasks = ast.literal_eval(links)
        return [task["TargetWorkItem"] for task in tasks if "TargetWorkItem" in task]