from enums.E_UserInputType import UserInputType

from models.tables.Table import *

class UserInputEventsTable(Table):
    '''
    Class UserInputEventsTable
    -------------------

    La clase UserInputEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)

        self._results = ResultsTable(["UI_NUM"] + \
                                     ["UI_NUM_TYPE_{0}".format(index.name) for index in UserInputType] + \
                                     ["UI_TIME"])


    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")
        

    def analyse_data(self):
        super().analyse_data()

        aux_results = {
            "UI_NUM": float(len(self._df)),
            "UI_NUM_GP_STEPS": 0.0,
            "UI_TIME": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list())
        }

        for index in UserInputType:
            aux_results["UI_NUM_TYPE_{0}".format(index.name)] = float(len(self._df[self._df["input_type"].str.upper() == index.name]))

        self._results.insert_row(aux_results)
#endregion
    
#region METODOS PRIVADOS
       

#enregion