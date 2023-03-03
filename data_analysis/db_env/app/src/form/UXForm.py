import pandas as pd

from form.Form import Form

class UXForm(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        aux_dict = {'id': [row["Identificador"].upper() for row_index, row in df.iterrows()]}

        for col_index in range(3, 93):
            aux_dict["quest_" + str(col_index - 3)] = df.iloc[:, col_index]

        self._df = pd.DataFrame(aux_dict)