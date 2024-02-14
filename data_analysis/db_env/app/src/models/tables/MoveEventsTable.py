from models.tables.Table import *
import matplotlib as plt

class MoveEventsTable(Table):
    
    #region VARIABLES PUBLICAS

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)

        self._results = ResultsTable(["MV_NUM_VR", "MV_NUM_RL",
                                      "MV_TIME_VR", "MV_TIME_RL", 
                                      "MV_DIST_VR", "MV_DIST_RL"])

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)        
        
        self._df["start_datetime"] = pd.to_datetime(self._df["start_datetime"], format="%Y-%m-%d %H:%M:%S")
        self._df["end_datetime"] = pd.to_datetime(self._df["end_datetime"], format="%Y-%m-%d %H:%M:%S")
        
    def analyse_data(self) -> None:
        super().analyse_data()


        aux_results = {
            "MV_NUM_VR": float(len(self._df[self._df["move_type"] == "virtual_reality"])),
            "MV_NUM_RL": float(len(self._df[self._df["move_type"] == "real_life"])), 
            "MV_TIME_VR": 0.0,
            "MV_TIME_RL": 0.0,
            "MV_DIST_VR": round(sum([float(dist) for dist in self._df[self._df["move_type"] == "virtual_reality"]["distance"].to_list()]), 2), 
            "MV_DIST_RL": round(sum([float(dist) for dist in self._df[self._df["move_type"] == "real_life"]["distance"].to_list()]), 2),
        }

        self._results.insert_row(aux_results)
    
    def create_graphs(self):
        super().create_graphs()

        self._vrgraphs = []

        #self.create_rw_movement_graph()
        self.create_vr_movement_graph()        

    #endregion

    #region METODOS PRIVADOS
        
    def clean_initial_dataframe(self):
        super().clean_initial_dataframe()

        self._df = self._df[self._df["distance"] < 10.0]
        self._df = self._df[self._df["scenario_type"] != "MainMenu"]
        self._df = self._df[self._df["scenario_type"] != "LoadingScreen"]
        self._df = self._df[self._df["scenario_type"] != "PlayerScore"]
        
    def create_vr_movement_graph(self):
        location_list = self._df[self._df["move_type"] == "virtual_reality"]["end_position"].to_list()

        x = []
        y = []

        for loc in location_list:
            newLoc = loc[1:-1].split(";")
            x.append(float(newLoc[0]))
            y.append(float(newLoc[1]))

        plt.scatter(y,x)
        self._vrgraphs.append(plt.gcf())
        #plt.show()
        
    def create_rw_movement_graph(self):
        location_list = self._df[self._df["move_type"] == "real_life"]["end_position"].to_list()

        x = []
        y = []

        for loc in location_list:
            newLoc = loc[1:-1].split(";")
            x.append(float(newLoc[0])*-1)
            y.append(float(newLoc[1])*-1)

        plt.xlim(-135, 135)
        plt.ylim(-100, 100)

        plt.scatter(y,x)
        #plt.show()
    #endregion