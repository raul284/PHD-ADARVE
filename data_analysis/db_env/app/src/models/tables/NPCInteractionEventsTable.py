from enums.E_NPCType import NPCType
from enums.E_NPCInteractionType import NPCInteractionType

from models.tables.Table import *

class NPCInteractionEventsTable(Table):
    
    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)

        self._results = ResultsTable(["NPC_NUM"] + \
                ["NPC_NUM_ACTOR_{0}".format(index) for index in range(len(NPCType))] + \
                    ["NPC_NUM_TYPE_{0}".format(index.name) for index in NPCInteractionType] + \
                    ["NPC_TIME_INTER"])

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)
        
        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")
        
    def analyse_data(self) -> None:
        super().analyse_data()
    
        aux_results = {
            "NPC_NUM": float(len(self._df)),
            "NPC_NUM_GP_STEPS": 0.0,
            "NPC_TIME_INTER": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list())
        }

        for index in range(len(NPCType)):
            aux_results["NPC_NUM_ACTOR_{0}".format(index)] = float(len(self._df[self._df["actor_id"] == index]))

        for index in NPCInteractionType:
            aux_results["NPC_NUM_TYPE_{0}".format(index.name)] = float(len(self._df[self._df["event_type"].str.upper() == index.name]))

        self._results.insert_row(aux_results)


    