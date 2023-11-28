import re
import pandas as pd


# should this be a dataclass?
class RegexFieldFilter:
    def __init__(self, field: str, pattern: re.Pattern):
        self.field = field
        self.pattern = pattern

    def filter(self, frame: pd.DataFrame) -> pd.DataFrame:
        pass
