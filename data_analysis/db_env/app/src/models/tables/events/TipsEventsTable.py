from models.tables.events.Table import *

class TipsEventsTable(Table):
    '''
    Class TipsEventsTable
    -------------------

    La clase TipsEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    _enabled: bool
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)
        
        self._results = ResultsTable(self._table_name, ["num_of_tips", "time_btw_tips"])

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