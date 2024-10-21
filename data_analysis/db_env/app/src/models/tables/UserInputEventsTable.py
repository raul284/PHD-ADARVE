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

    def read_data_from_csv(self) -> None:
        super().read_data_from_csv()

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        

    def analyse_data(self):
        super().analyse_data()


    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        results = {}
        results["UI_NUM"] = float(len(df))
        for index in UserInputType:
            results["UI_NUM_TYPE_{0}".format(index.name)] = float(len(df[df["input_type"].str.upper() == index.name]))
        results["UI_TIME"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        return results


    def create_graphs(self):
        pass

#endregion
    
#region METODOS PRIVADOS
       
    def clean_initial_dataframe(self):
        super().clean_initial_dataframe()

#enregion