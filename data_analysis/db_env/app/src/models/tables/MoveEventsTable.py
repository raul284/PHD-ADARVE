from models.tables.Table import *

class MoveEventsTable(Table[T]):
    
    #region VARIABLES PUBLICAS

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, generic_type: Type[T]) -> None:
        super().__init__(generic_type=generic_type)

        self._results = ResultsTable(["[MOVE]num_of_vw", "[MOVE]distance_vw", "[MOVE]num_of_rw", "[MOVE]distance_rw"])

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)
        
        self._df["start_datetime"] = pd.to_datetime(self._df["start_datetime"], format="%Y-%m-%d %H:%M:%S")
        self._df["end_datetime"] = pd.to_datetime(self._df["end_datetime"], format="%Y-%m-%d %H:%M:%S")
        
    def analyse_data(self) -> None:
        super().analyse_data()

        aux_results = {
            "[MOVE]num_of_vw": len(self._df[self._df["move_type"] == "virtual_reality"]),
            "[MOVE]distance_vw": round(sum([float(dist) for dist in self._df[self._df["move_type"] == "virtual_reality"]["distance"].to_list()]), 2), 
            "[MOVE]num_of_rw": len(self._df[self._df["move_type"] == "real_life"]), 
            "[MOVE]distance_rw": round(sum([float(dist) for dist in self._df[self._df["move_type"] == "real_life"]["distance"].to_list()]), 2),
        }

        self._results.insert_row(aux_results)
    
    def create_graphs(self):
        super().create_graphs()

        #self.create_rw_movement_graph()
        self.create_vr_movement_graph()
        

    #endregion

    #region METODOS PRIVADOS
        
    def create_vr_movement_graph(self):
        location_list = self._df[self._df["move_type"] == "virtual_reality"]["end_position"].to_list()

        x = []
        y = []

        for loc in location_list:
            newLoc = loc[1:-1].split(";")
            x.append(float(newLoc[0]))
            y.append(float(newLoc[1]))

        plt.scatter(y,x)
        plt.show()
        
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