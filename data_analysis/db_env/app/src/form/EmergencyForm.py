import pandas as pd

from form.Form import Form

class EmergencyForm(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        self._df = pd.DataFrame({'id': [row["Identificador"].upper() for row_index, row in df.iterrows()],
            'emergency_know': self.tanslate_simpleafirmations_to_pc([row["¿Sabes qué es una emergencia radiológica?"] for row_index, row in df.iterrows()]),
            'emergency_desc': [row["Describe qué es una emergencia radiológica."] for row_index, row in df.iterrows()]
        })