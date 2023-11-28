import pandas as pd


class CompositeFilter:
    def __init__(self, filters):
        self.filters = filters

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        # won't this duplicate the data frame for each intermediate filter?
        filtered_df = df
        for fil in self.filters:
            filtered_df = fil.filter(filtered_df)
        return filtered_df
