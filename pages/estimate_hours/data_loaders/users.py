from pages.estimate_hours.data_loaders.work_items import WorkItems
import pandas as pd
import ast

class Users(WorkItems):
    
    def __init__(self) -> None:
        super().__init__()
        user_names = set(self.data["UserName"].dropna().unique())
        
        all_tasks = []
        for links in self.data["Links"]:
            all_tasks.extend(self.extract_tasks(links))
            
        tasks = pd.DataFrame(all_tasks)
        
        for links in self.data["Links"]:
            tasks = ast.literal_eval(links)
            for task in tasks:
                assigned = task.get("TargetWorkItem", {}).get("AssignedTo", {})
                user = assigned.get("UserName")
                if user:
                    user_names.add(user)
                    
        self.data = pd.DataFrame({"UserName": sorted(list(user_names))})