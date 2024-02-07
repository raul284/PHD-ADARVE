from enums.E_UserInputType import UserInputType

from models.tables.Table import *

class UserInputEventsTable(Table[T]):
    '''
    Class UserInputEventsTable
    -------------------

    La clase UserInputEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, generic_type: Type[T]) -> None:
        super().__init__(generic_type=generic_type)

        self._results = ResultsTable(["[USER_INPUT]num_of_inputs", "[USER_INPUT]time_btw_inputs"] + \
                                     ["[USER_INPUT]num_of_inputs_type_{0}".format(index.name) for index in UserInputType]) # Por cada tipo de user input


    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")
        

    def analyse_data(self):
        super().analyse_data()

        aux_results = {
            "[USER_INPUT]num_of_inputs": len(self._df),
            "[USER_INPUT]time_btw_inputs": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list()) 
        }

        for index in UserInputType:
            aux_results["[USER_INPUT]num_of_inputs_type_{0}".format(index.name)] = len(self._df[self._df["input_type"].str.upper() == index.name])

        self._results.insert_row(aux_results)
#endregion
    
#region METODOS PRIVADOS
       

#enregion