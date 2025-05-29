from pages.estimate_hours.data_loaders.user_stories import UserStories
from pages.estimate_hours.data_loaders.tasks import Tasks
import pandas as pd
import re

class IterationPath:
    
    def __init__(self) -> None:
        super().__init__()
        pattern = r"^\d{4}_S\d{2}_[A-Za-z]{3}\d{2}-[A-Za-z]{3}\d{2}$"
        paths = []
        user_stories = UserStories().data
        user_stories = user_stories[user_stories["EstimateHours"] != 0]
        user_stories_paths = set(user_stories["IterationPath"].dropna().unique())
        
        for path in user_stories_paths:
            date = path.split('\\')[-1]
            if re.match(pattern, date):
                paths.append(path)
            
        
        tasks = Tasks().data
        tasks = tasks[tasks["OriginalEstimate"] != 0]
        tasks_paths = set(tasks["IterationPath"].dropna().unique())
        
        for path in tasks_paths:
            date = path.split('\\')[-1]
            if re.match(pattern, date):
                paths.append(path)
    
        self.data = pd.DataFrame({"IterationPath": paths})