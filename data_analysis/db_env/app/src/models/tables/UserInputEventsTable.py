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

    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="user_input")


    def set_data(self) -> None:
        super().set_data()

    def read_data(self) -> None:
        super().read_data()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        
    def analyse_data(self):
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        return super().analyse_df(df)
        
    def analyse_number(self, df):
        results = {}

        results["UI_N"] = float(len(df))

        for index in UserInputType:
            results["UI_N_t_{0}".format(index.value)] = float(len(df[df["input_type"].str.upper() == index.name]))

        return results

    
    def analyse_time(self, df):
        results = {}

        results["UI_T"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        return results


    def create_graphs(self):
        pass

#endregion
    
#region METODOS PRIVADOS
       

#enregion