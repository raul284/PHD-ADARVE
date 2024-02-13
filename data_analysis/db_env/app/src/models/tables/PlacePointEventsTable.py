from models.tables.Table import *

class PlacePointEventsTable(Table):
    '''
    Class PlacePointEventsTable
    -------------------

    La clase PlacePointEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)

        self._results = ResultsTable(["", ""])

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")
        
#endregion
    
#region METODOS PRIVADOS
       

#enregion