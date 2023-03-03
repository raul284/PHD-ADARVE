import pandas as pd

class Form:

    _df: pd.DataFrame

    def __init__(self):
        pass

    def from_csv(self, filename: str):
        self._df = pd.read_csv(filename)

    def from_json(self, filename: str):
        self._df = pd.read_json(filename)

    def from_excel(self, filename: str):
        self._df = pd.read_excel(filename)

    def from_dataframe(self, df: pd.DataFrame):
        pass

    def to_json(self, filename: str):
        self._df.to_json(filename)

    def to_csv(self, filename: str):
        self._df.to_csv(filename, index=False)

    def tanslate_simpleafirmations_to_pc(self, values: list):
        result = []
        for val in values:
            if val == "Sí": result.append("yes")
            elif val == "No": result.append("no")
            elif val == "Tal vez": result.append("maybe")
        return result


        

    








