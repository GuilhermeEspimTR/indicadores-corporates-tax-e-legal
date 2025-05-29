from pandas import DataFrame

class Graph:
    
    df: DataFrame = DataFrame()
    original_df: DataFrame = DataFrame()
  
    def filter_data_frame(self, column, values):
        if values or self.df.empty:
            self.df = self.df[self.df[column].isin(values)]
        else:
            self.df = self.original_df.data.dropna(subset=['OriginalEstimate'])