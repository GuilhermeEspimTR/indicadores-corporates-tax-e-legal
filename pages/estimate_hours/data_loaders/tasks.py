from pages.estimate_hours.data_loaders.work_items import WorkItems
import pandas as pd
import ast
import re


class Tasks(WorkItems):
    
    def __init__(self) -> None:
        super().__init__()
        all_tasks = []
        for links in self.data["Links"]:
            all_tasks.extend(self.extract_tasks(links))
        
        self.data = pd.DataFrame(all_tasks)
        
        self.data['UserName'] = self.data['AssignedTo'].apply(self.extract_user_name)
        
        self.data['CreatedOn'] = self.data['CreatedOn'].apply(self.extract_date)
        self.data['CreatedOn'] = pd.to_datetime(self.data['CreatedOn'], errors='coerce')
        self.data = self.data.rename(columns={'CreatedOn': 'CreatedDate'})
        
        self.data = self.data.sort_values(by=['UserName', 'CreatedDate'])
        
        self.data["IterationPath"] = self.data["Iteration"].apply(self.extract_iteration_path)
        
        col = self.data['IterationPath'].astype(str).str.split('\\').str[-1]

        pattern = r"^\d{4}_S\d{2}_[A-Za-z]{3}\d{2}-[A-Za-z]{3}\d{2}$"

        self.data['SprintDate'] = col.apply(lambda x: x if re.match(pattern, x) else None)
    
    
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