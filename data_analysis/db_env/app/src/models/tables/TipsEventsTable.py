from models.tables.Table import *

class TipsEventsTable(Table[T]):
    '''
    Class TipsEventsTable
    -------------------

    La clase TipsEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    _enabled: bool
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, generic_type: Type[T], tips_ingame_enabled) -> None:
        super().__init__(generic_type=generic_type)
        self._enabled = tips_ingame_enabled

        self._results = ResultsTable(["[TIPS]num_of_tips", "[TIPS]time_btw_tips"])

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")

    def analyse_data(self):
        super().analyse_data()

        if self._enabled:
            aux_results = {
                "[TIPS]num_of_tips": len(self._df),
                "[TIPS]time_btw_tips": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list()) 
            }
        else:
            aux_results = {
                "[TIPS]num_of_tips": 0,
                "[TIPS]time_btw_tips": 0 
            }

        self._results.insert_row(aux_results)
        
#endregion
    
#region METODOS PRIVADOS
       

#enregion