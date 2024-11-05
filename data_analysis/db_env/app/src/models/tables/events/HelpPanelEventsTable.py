from models.tables.events.Table import *
from enums.E_TutorialItemType import TutorialItemType

class HelpPanelEventsTable(Table):
    '''
    Class HelpPanelEventsTable
    ------------------------------
    '''

    #region VARIABLES PUBLICAS

    #endregion
    
    #region METODOS PUBLICOS

    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="help_panel")

    # __init__

    def set_data(self) -> None:
        super().set_data()

    def read_data(self) -> None:
        super().read_data()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")

    # read_data_from_csv


    def analyse_data(self) -> None:
        super().analyse_data()
    
    # analyse_data

    def analyse_df(self, df) -> dict:
        results = {}
        return {**results, **self.analyse_number(df), **self.analyse_time(df)}
    
    def analyse_number(self, df):
        results = {}

        results["HP_N"] = len(df[df["event_type"] == "open"])
        results["HP_N_I"] = len(df[df["event_type"] == "demand_help"])
        results["HP_N_SI"] = self.get_help_per_activation(df)

        for index in TutorialItemType:
            results["HP_N_t_{0}".format(index.value)] = len(df[df["tutorial_item_id"] == index.name])

        return results
    
    def analyse_time(self, df):
        results = {}

        results["HP_T"] = self.get_time_per_activation(df)
        results["HP_T_I"] = 0

        print(results)

        return results
        
    def create_graphs(self):
        pass

    #endregion
        
    #region METODOS PRIVADOS    

    def get_help_per_activation(self, df):
        result_list = []

        count = 0
        for index, row in df.iterrows():
            if row["event_type"] == "demand_help":
                count += 1
            elif row["event_type"] == "close": 
                if count > 0: result_list.append(count)
                count = 0

        if result_list:
            return round(statistics.mean(result_list), 3)
        else: return 0

    def get_time_per_activation(self, df):
        times = []

        open_time = None
        close_time = None
        activate_timer = False

        for index, row in df.iterrows():
            if row["event_type"] == "open":
                open_time = row["event_datetime"] 
            elif row["event_type"] == "demand_help":
                activate_timer = True
            elif row["event_type"] == "close": 
                if activate_timer: 
                    self.get_time_btw_datetimes(open_time, row["event_datetime"])
                    activate_timer = False
                else: 
                    open_time = None

        if times:
            return round(statistics.mean(times), 3)
        else: return 0

    def get_time_per_info(df):
        pass

    #endregion
        


    