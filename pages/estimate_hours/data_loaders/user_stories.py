from pages.estimate_hours.data_loaders.work_items import WorkItems

class UserStories(WorkItems):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.data = self.data[self.data["WorkItemType"] == "User Story"]
        self.data = self.data.drop(["WorkItemType"], axis=1)