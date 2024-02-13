import pandas as pd
from datetime import datetime
import statistics

class ResultsTable():
    '''
    Class ResultsTable
    -------------------

    La clase ResultsTable ...
    '''
#region VARIABLES GLOBALES
    
    _df: pd.DataFrame

#endregion
    
#region METODOS PUBLICOS

    def __init__(self, col_names) -> None:
        self._df = pd.DataFrame(columns=["{0}".format(name) for name in col_names])

    def analyse_data(self):
        pass

    def export_results(self):
        pass

    def insert_row(self, data):
        self._df.loc[len(self._df)] = data

    def get_time_btw_datetimes(self, datetimes_list) -> float:
        # Iniciamos una lista vacia donde se irá almacenando el tiempo entre interacciones.
        times_btw = []
        # Por cada uno de los eventos de la lista
        for index in range(len(datetimes_list) - 1):
            # Se resta el tiempo del evento siguiente y del actual
            rest = int(datetimes_list[index + 1].timestamp()) - int(datetimes_list[index].timestamp())
            # El resto se almacena en la lista
            times_btw.append(rest)

        # Se calcula la media de la lista
        return round(statistics.mean(times_btw), 2)


#endregion
    
#region METODOS PRIVADOS
       

#enregion