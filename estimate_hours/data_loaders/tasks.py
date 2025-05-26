from estimate_hours.data_loaders.work_items import WorkItems


class Tasks(WorkItems):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.data = self.data[self.data["WorkItemType"] == "Task"]
        self.data = self.data.drop(["WorkItemType"], axis=1)