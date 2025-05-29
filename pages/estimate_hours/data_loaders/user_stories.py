from pages.estimate_hours.data_loaders.work_items import WorkItems
import ast
import pandas as pd

class UserStories(WorkItems):
    
    def __init__(self) -> None:
        super().__init__()
        self.data["EstimateHours"] = self.data["Links"].apply(self.sum_estimates)
        self.data["CreatedDate"] = self.data["Links"].apply(self.get_first_task_created_on)
        self.data = self.data[
            ["WorkItemId", "Title", "State", "WorkItemType", "CreatedDate", "EstimateHours", "UserName", "AssignedTo", "IterationPath", "SprintDate", "Iteration"]
        ]
        
    
    def sum_estimates(self, links_str):
        tasks = ast.literal_eval(links_str)
        return sum(
            task["TargetWorkItem"].get("OriginalEstimate") or 0
            for task in tasks if "TargetWorkItem" in task
        )
        
        
    def get_first_task_created_on(self, links_str):
        try:
            tasks = ast.literal_eval(links_str)
            # Extrai todas as datas de criação das tasks
            dates = [
                task["TargetWorkItem"].get("CreatedOn", {}).get("Date")
                for task in tasks
                if "TargetWorkItem" in task and task["TargetWorkItem"].get("CreatedOn", {}).get("Date")
            ]
            # Retorna a menor data (primeira task criada), ou None se não houver
            if dates:
                return min(pd.to_datetime(dates))
            else:
                return None
        except Exception:
            return None
        