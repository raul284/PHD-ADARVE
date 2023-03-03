import pandas as pd

from form.Form import Form

class DGD1Form(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        self._df = pd.DataFrame({'id': [row["Identificador"].upper() for row_index, row in df.iterrows()],
                'conqueror': self.translate_style_to_pc([row["¿Te sientes identificado por ellos? [Conqueror]"] for row_index, row in df.iterrows()]),
                'manager': self.translate_style_to_pc([row["¿Te sientes identificado por ellos? [Manager]"] for row_index, row in df.iterrows()]),
                'wanderer': self.translate_style_to_pc([row["¿Te sientes identificado por ellos? [Wanderer]"] for row_index, row in df.iterrows()]),
                'participant': self.translate_style_to_pc([row["¿Te sientes identificado por ellos? [Participant]"] for row_index, row in df.iterrows()])
            })

    def translate_style_to_pc(self, values):
        result = []
        for val in values:
            if val == "No significativamente": result.append("0")
            elif val == "Ligeramente": result.append("1")
            elif val == "Moderadamente": result.append("2")
            elif val == "Fuertemente": result.append("3")
            elif val == "Predominantemente": result.append("4")
        return result