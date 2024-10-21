from models.tables.Table import *

class MoveEventsTable(Table):
    
    #region VARIABLES PUBLICAS

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, user_data) -> None:
        super().__init__(user_data=user_data, table_name="move")

    def set_data(self) -> None:
        super().set_data()

    def read_data_from_csv(self) -> None:
        super().read_data_from_csv()        

        self._df["start_datetime"] = pd.to_datetime(self._df["start_datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        self._df["end_datetime"] = pd.to_datetime(self._df["end_datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        
    def analyse_data(self) -> None:
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        return {
            "MV_NUM_VR": float(len(df[df["move_type"] == "virtual_reality"])),
            "MV_NUM_RL": float(len(df[df["move_type"] == "real_life"])), 
            "MV_DIST_VR": round(sum([float(dist) for dist in df[df["move_type"] == "virtual_reality"]["distance"].to_list()]), 2), 
            "MV_DIST_RL": round(sum([float(dist) for dist in df[df["move_type"] == "real_life"]["distance"].to_list()]), 2),
        }
    
    def create_graphs(self):
        pass  

    #endregion

    #region METODOS PRIVADOS
        
    def clean_initial_dataframe(self):
        super().clean_initial_dataframe()
        self._df = self._df[self._df["distance"] < 10.0]
        self._df = self._df.drop(self._df[self._df["start_datetime"] == "1-1-1 0:0:0.0"].index)
        
    #endregion