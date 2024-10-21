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

    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="place_point")

    # __init__

    def set_data(self) -> None:
        super().set_data()

    def read_data_from_csv(self) -> None:
        super().read_data_from_csv()

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        
        
    def analyse_data(self) -> None:
        super().analyse_data()
    
    # analyse_data

    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        results = {}

        return results
    
#endregion
    
#region METODOS PRIVADOS
       

#enregion