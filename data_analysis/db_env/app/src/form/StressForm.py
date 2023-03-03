import pandas as pd

from form.Form import Form

class StressForm(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        stress = {}

        for row_index, row in df.iterrows():
            if not 'id' in stress:
                stress['id'] = []
            stress['id'].append(row["Identificador"].upper())
            for stress_index in range(len(df.columns) - 14, len(df.columns)):
                if not "quest_" + str(stress_index - 13) in stress:
                    stress["quest_" + str(stress_index - 13)] = []
                stress["quest_" + str(stress_index - 13)].append(self.cuantitative_stress_quest(df.iloc[row_index, stress_index]))

        self._df = pd.DataFrame(stress)



    def cuantitative_stress_quest(self, value):
        if value == "Nunca": return 0
        elif value == "Casi nunca": return 1
        elif value == "De vez en cuando": return 2
        elif value == "A menudo": return 3
        elif value == "Muy a menudo": return 4