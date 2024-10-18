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



#endregion
    
#region METODOS PRIVADOS
       

#enregion