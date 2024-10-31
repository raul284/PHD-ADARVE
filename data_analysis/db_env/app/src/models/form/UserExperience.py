import pandas as pd


class UserExperience():
    '''
    Class UserExperience
    ----------------------------------------
    Clase que gestiona el cálculo de la experiencia de usuario. Para ello se está utilizando el UEQ (https://www.ueq-online.org).
    
    Este cuestionario está formado por 6 rasgos:
    - Attractiveness:
    - Perspicuity:
    - Efficiency:
    - Dependability:
    - Stimulation:
    - Novelty:

    El cuestionario está compuesto por un total de 26 preguntas con escala likert [-3, 3]. El cálculo se realiza sumando el valor
    de las respuestas relacionadas con cada uno de los 6 rasgos y dividirlo por la cantidad de preguntas, es decir, un cálculo medio sencillo.

    Nota: Este código está pensado para una escala likert del 1 al 7 por lo que simplemente se le restará 4 a la respuesta (1-4=-3 y 7-4=3).
    
    '''

    _data: pd.DataFrame
    _traits_ids: dict

    _results: dict

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._results = {}

        self._traits_ids = {
            "attractiveness": [0, 11, 13, 15, 23, 24],
            "perspicuity": [1, 3, 12, 20],
            "efficiency": [8, 19, 21, 22],
            "dependability": [7, 10, 16, 18],
            "stimulation": [4, 5, 6, 17],
            "novelty": [2, 9, 14, 25]
        }

    def calculate(self):
        for trait in self._traits_ids:
            # El número de preguntas asociada al factor. Se usa para el cálculo de la media
            trait_len = len(self._traits_ids[trait])
            # La suma de los valores de las preguntas. Se le resta 4 a cada valor porque nuestros datos tienen un rango de [1, 7] y deberían estar en [-3, 3]
            sum_of_scores = sum([self._data[self._data.columns[id]].iloc[0] - 4 for id in self._traits_ids[trait]])

            # Se hace la media y se redondea
            score_by_trait = round(sum_of_scores / trait_len, 3)
            self._results["UX_{0}".format(trait[0].upper())] = float(score_by_trait)

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self._results, index=[0])