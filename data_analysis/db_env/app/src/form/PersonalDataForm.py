import pandas as pd

from form.Form import Form

class PersonalDataForm(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        self._df = pd.DataFrame({'id': [row["Identificador"].upper() for row_index, row in df.iterrows()],
                'age': [row["Edad"] for row_index, row in df.iterrows()],
                'sex': self.translate_sex_to_pc([row["Género"] for row_index, row in df.iterrows()]),
                'education': self.translate_education_to_pc([row["Educación"] for row_index, row in df.iterrows()])
            })

    def translate_sex_to_pc(self, values):
        result = []
        for val in values:
            if val == "Hombre": result.append("man")
            elif val == "Mujer": result.append("woman")
            elif val == "No binario": result.append("non_binary")
            elif val == "Prefiero no decirlo": result.append("no_answer")
        return result

    def translate_education_to_pc(self, values):
        result = []
        for val in values:
            if val == "Educación primaria": result.append("primary")
            elif val == "Educación secundaria": result.append("secundary")
            elif val == "Bachillerato": result.append("bach")
            elif val == "Formación profesional": result.append("fp")
            elif val == "Grado universitario": result.append("degree")
            elif val == "Máster universitario": result.append("master")
            elif val == "Doctorado": result.append("phd")
        return result

    