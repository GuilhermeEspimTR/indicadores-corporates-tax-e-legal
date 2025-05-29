from pages.estimate_hours.data_loaders.iteration_path import IterationPath
import re
import pandas as pd
import ast

class Sprints(IterationPath):
    
    def __init__(self) -> None:
        super().__init__()
        sprints_date = set(self.data["IterationPath"].dropna().unique())
        
        all_dates = []
        
        for item in sprints_date:
            pattern = r"^\d{4}_S\d{2}_[A-Za-z]{3}\d{2}-[A-Za-z]{3}\d{2}$"
            date = item.split('\\')[-1]
            if re.match(pattern, date):
                all_dates.append(date)

    
                    
        self.data = pd.DataFrame({"SprintDate": list(all_dates)})
        self.data = self.data.drop_duplicates(subset=["SprintDate"]).dropna(subset=["SprintDate"])