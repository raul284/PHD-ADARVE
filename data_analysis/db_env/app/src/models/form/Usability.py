import pandas as pd

class Usability():
    '''
    Class Usability
    ----------------------------------------
    Clase que gestiona el cálculo de la usabilidad de la aplicación. Para ello se está utilizando el SUS (https://uxls.org/methods/system-usability-scale/).

    El cuestionario está compuesto por un total de 10 preguntas con escala likert [1, 5]. El cálculo se realiza:
    - X = (Suma de todos los valores impares) - 5
    - Y = 25 - (Suma de todos los valores pares)
    - Score = (X + Y) * 2.5
    
    '''

    _data: pd.DataFrame

    _results: dict

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._results = {}

    def calculate(self):
        # Para coger los valores pares e impares se hace de manera inversa haciendo a la inversa. Los 
        # índices pares en programación serían el 0, 2, 4...pero en la vida real esto se traduce en 
        # 1, 3, 5... Lo que nosotros queremos seleccionar son los valores reales (2, 4, 6...) los cuales 
        # son los impares en programación. Por ello, estoy pillando los índices al contrario.
        x = sum([self._data[col].iloc[0] for col in self._data.columns[::2]]) - 5.0
        y = 25.0 - sum([self._data[col].iloc[0] for col in self._data.columns[1::2]])

        self._results["SUS"] = (x + y) * 2.5

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self._results, index=[0])