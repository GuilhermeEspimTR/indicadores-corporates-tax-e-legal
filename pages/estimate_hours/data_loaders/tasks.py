from pages.estimate_hours.data_loaders.work_items import WorkItems
import pandas as pd
import ast


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