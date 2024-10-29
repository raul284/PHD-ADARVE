import statistics

from models.tables.events.Table import *


class TutorialTaskEventsTable(Table):
    '''
    Class TutorialTaskEventsTable
    ------------------------------
    '''

    #region VARIABLES PUBLICAS

    #endregion
    
    #region METODOS PUBLICOS

    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="tutorial_task")

    # __init__

    def set_data(self) -> None:
        super().set_data()

    def read_data(self) -> None:
        super().read_data()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")

    # read_data


    def analyse_data(self) -> None:
        super().analyse_data()
    
    # analyse_data

    def analyse_df(self, df) -> dict:
        return super().analyse_df(df)
    
    def analyse_number(self, df):
        results = {}
        return results
    
    def analyse_time(self, df):
        results = {}

        results["TT_T"] = self.get_time_btw_two_type(df[df["event_type"] == "started"], df[df["event_type"] == "completed"], ["tutorial_item_id"])

        return results
        
    def create_graphs(self):
        pass

    #endregion
        
    #region METODOS PRIVADOS    

    #endregion
        


    