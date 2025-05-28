from pages.estimate_hours.data_loaders.work_items import WorkItems
import ast

class UserStories(WorkItems):
    
    def __init__(self) -> None:
        super().__init__()
        self.data["EstimateHours"] = self.data["Links"].apply(self.sum_estimates)
        self.data = self.data[
            ["WorkItemId", "Title", "State", "WorkItemType", "CreatedDate", "EstimateHours", "UserName", "AssignedTo"]
        ]
        
    
    def sum_estimates(self, links_str):
        tasks = ast.literal_eval(links_str)
        return sum(
            task["TargetWorkItem"].get("OriginalEstimate") or 0
            for task in tasks if "TargetWorkItem" in task
        )
        