import pandas as pd

class PersonalData():

    _data: pd.DataFrame
    _results: dict
    
    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._results = {}

    def analyse_data(self):
        aux_dict = self._data.to_dict('records')[0]
        for key in aux_dict:
            if "Edad" in key:
                self._results["AGE"] = aux_dict[key]
            elif "Género" in key:
                self._results["GENRE"] = self.translate_genre(aux_dict[key])
            elif "Educación" in key:
                self._results["EDU"] = aux_dict[key]
            elif "realidad virtual" in key:
                self._results["VR_FREQUENCY"] = aux_dict[key]

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self._results, index=[0])
    
    def translate_genre(self, genre):
        if genre == "Hombre":
            return "H"
        elif genre == "Mujer":
            return "M"
        elif genre == "No binario":
            return "NB"
        elif genre == "Prefiero no decirlo":
            return "Undefined"
        else:
            return "O"

                
    
