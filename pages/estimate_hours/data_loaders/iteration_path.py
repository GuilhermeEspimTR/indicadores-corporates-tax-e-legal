from pages.estimate_hours.data_loaders.work_items import WorkItems
import pandas as pd
import ast

class IterationPath(WorkItems):
    
    def __init__(self) -> None:
        paths = set(self.data["IterationPath"].dropna().unique())
        
        all_tasks = []
        for links in self.data["Links"]:
            all_tasks.extend(self.extract_iteration_paths(links))
            
        tasks = pd.DataFrame(all_tasks)
        for links in self.data["Links"]:
            tasks = ast.literal_eval(links)
            for task in tasks:
                iteration_path = task.get("TargetWorkItem", {}).get("Iteration", {}).get("IterationPath")
                if iteration_path:
                    paths.add(iteration_path)
        
        self.data = pd.DataFrame({"IterationPath": list(paths)})