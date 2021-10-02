
import pandas as pd
import numpy as np

from util.analysis import Loader

class CsvLoader(Loader):
    """
    Class for loading fitness data
    """
    def __init__(self, path: str):
        super().__init__(path)
        self.df = None

    def load(self) -> bool:
        try:
            self.df = pd.read_csv(self.path + "/fitness_data.csv", index_col=0)
            return True
        except Exception:
            print("Exception")
            return False

    def as_numpy(self) -> np.array:
        if self.df is not None:
            return self.df.to_numpy()
        return np.array([])

    def as_df(self) -> pd.DataFrame:
        if self.df is not None:
            return self.df
        return pd.DataFrame([])
