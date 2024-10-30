from models.tables.events.Table import *

class MoveEventsTable(Table):
    
    #region VARIABLES PUBLICAS

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, user_data) -> None:
        super().__init__(user_data=user_data, table_name="move")

    def set_data(self) -> None:
        super().set_data()

    def read_data(self) -> None:
        super().read_data()        

        self._df = self._df[self._df["distance"] < 10.0]
        self._df = self._df.drop(self._df[self._df["start_datetime"] == "1-1-1 0:0:0.0"].index)

        self._df["start_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["start_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        self._df["end_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["end_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        
    def analyse_data(self) -> None:
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        return super().analyse_df(df)

    def analyse_number(self, df) -> dict:
        results = {}

        results["MV_N_VR"] =  float(len(df[df["move_type"] == "virtual_reality"]))
        results["MV_N_RL"] = float(len(df[df["move_type"] == "real_life"]))

        # Distancia total recorrida
        results["MV_DT_VR"] = round(df[df["move_type"] == "virtual_reality"]["distance"].sum(), 3)
        results["MV_DT_RL"] = round(df[df["move_type"] == "real_life"]["distance"].sum(), 3)

        # Distancia media por cada desplazamiento
        results["MV_DM_VR"] = round(df[df["move_type"] == "virtual_reality"]["distance"].mean(), 3)
        results["MV_DM_RL"] = round(df[df["move_type"] == "real_life"]["distance"].mean(), 3)

        return results
    
    def analyse_time(self, df) -> dict:
        results = {}

        # Tiempo medio entre teletransportes
        results["MV_T_VR"] = self.get_time_btw_move(df[df["move_type"] == "virtual_reality"])
        # Tiempo medio entre movimientos en la vida real
        results["MV_T_RL"] = self.get_time_btw_move(df[df["move_type"] == "real_life"])

        # Tiempo medio entre que inicia el teletransporte y lo termina
        results["MV_T_TE"] = self.get_time_teleport(df[df["move_type"] == "virtual_reality"])

        return results
    
    def create_graphs(self):
        pass  

    #endregion

    #region METODOS PRIVADOS
        
    def get_time_btw_move(self, df):
        time_btw = []

        start_times = df["start_datetime"].to_list()
        end_times = df["end_datetime"].to_list()

        for i in range(1, len(df)):
            time_btw.append(start_times[i].timestamp() - end_times[i - 1].timestamp())

        return round(statistics.mean(time_btw), 3)


    def get_time_teleport(self, df):
        time_btw = []

        for index, row in df.iterrows():
            time_btw.append(row["end_datetime"].timestamp() - row["start_datetime"].timestamp())

        return round(statistics.mean(time_btw), 3)

        
    #endregion