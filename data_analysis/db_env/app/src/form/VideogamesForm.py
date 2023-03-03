import pandas as pd

from form.Form import Form

class VideogamesForm(Form):
    def __init__(self):
        super().__init__()

    def from_dataframe(self, df: pd.DataFrame):
        self._df = pd.DataFrame({'id': [row["Identificador"].upper() for row_index, row in df.iterrows()],
            'game_like': self.translate_gamelike_to_pc([row["¿Te gustan los videojuegos?"] for row_index, row in df.iterrows()]),
            'game_frecuency': self.translate_gamefrecuency_to_pc([row["¿Con cuánta frecuencia juegas?"] for row_index, row in df.iterrows()]),
            'vr_used': self.tanslate_simpleafirmations_to_pc([row["¿Has usado alguna vez unas gafas de realidad virtual?"] for row_index, row in df.iterrows()]),
            'vr_like': self.tanslate_simpleafirmations_to_pc([row["¿Te gustó la experiencia?"] for row_index, row in df.iterrows()]),
            'vr_sickness': self.tanslate_simpleafirmations_to_pc([row["¿Te mareaste?"] for row_index, row in df.iterrows()]),
            'vr_world': self.tanslate_simpleafirmations_to_pc([row["¿Sentías que estabas en otro mundo?"] for row_index, row in df.iterrows()]),
            'vr_again': self.translate_vragain_to_pc([row["¿Has vuelto a usar unas gafas de realidad virtual?"] for row_index, row in df.iterrows()])
        })

    def translate_gamelike_to_pc(self, values):
        result = []
        for val in values:
            if val == "Sí, mucho":
                result.append("lot")
            elif val == "Sí, un poco":
                result.append("little")
            elif val == "Indiferente":
                result.append("indiference")
            elif val == "No me gustan":
                result.append("no")
        return result

    def translate_gamefrecuency_to_pc(self, values):
        result = []
        for val in values:
            if val == "Todos los días" or val == "Casi todos los días":
                result.append("hardcore")
            elif val == "Una vez por semana" or val == "Una vez al mes":
                result.append("casual")
            elif val == "Una vez al año" or val == "Nunca":
                result.append("non_gamer")
        return result

    def translate_vragain_to_pc(self, values):
        result = []
        for val in values:
            if val == "Sí, las uso todos los días":
                result.append("everyday")
            elif val == "Sí, las uso a veces":
                result.append("sometimes")
            elif val == "Sí, las he usado un par de veces más":
                result.append("twice")
            elif val == "No":
                result.append("no")
        return result

    