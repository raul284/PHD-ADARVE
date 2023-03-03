import pandas as pd

from form.Form import Form

class ResultsForm(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        self._df = pd.DataFrame({'id': [row["Identificador"].upper() for row_index, row in df.iterrows()] })