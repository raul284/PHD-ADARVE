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
        return super().analyse_df(df)

    def analyse_number(self, df) -> dict:
        results = {}

        results["MV_N_VR"] =  float(len(df[df["move_type"] == "virtual_reality"]))
        results["MV_N_RL"] = float(len(df[df["move_type"] == "real_life"]))

        results["MV_D_VR"] = round(df[df["move_type"] == "virtual_reality"]["distance"].sum(), 3)
        results["MV_D_RL"] = round(df[df["move_type"] == "real_life"]["distance"].sum(), 3)

        return results
    
    def analyse_time(self, df) -> dict:
        results = {}

        # Tiempo medio entre teletransportes
        results["MV_T_VR"] = 0.0
        # Tiempo medio entre movimientos en la vida real
        results["MV_T_RL"] = 0.0

        # Tiempo medio entre que inicia el teletransporte y lo termina
        results["MV_T_TE"] = 0.0

        return results
    
    def create_graphs(self):
        pass  

    #endregion

    #region METODOS PRIVADOS
        
    def clean_initial_dataframe(self):
        super().clean_initial_dataframe()
        self._df = self._df[self._df["distance"] < 10.0]
        self._df = self._df.drop(self._df[self._df["start_datetime"] == "1-1-1 0:0:0.0"].index)
        
    #endregion