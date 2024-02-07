from models.tables.Table import *

class PlacePointEventsTable(Table[T]):
    '''
    Class PlacePointEventsTable
    -------------------

    La clase PlacePointEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, generic_type: Type[T]) -> None:
        super().__init__(generic_type=generic_type)

        self._results = ResultsTable(["", ""])

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")
        
#endregion
    
#region METODOS PRIVADOS
       

#enregion