from enums.E_NPCType import NPCType
from enums.E_NPCInteractionType import NPCInteractionType

from models.tables.Table import *

class NPCInteractionEventsTable(Table[T]):
    
    def __init__(self, generic_type: Type[T]) -> None:
        super().__init__(generic_type=generic_type)

        self._results = ResultsTable(
            ["[NPC_INTERACTION]num_of_interactions", "time_btw_interactions"] + \
                ["[NPC_INTERACTION]num_of_interactions_with_actor_{0}".format(index) for index in range(len(NPCType))] + \
                    ["[NPC_INTERACTION]num_of_interactions_type_{0}".format(index.name) for index in NPCInteractionType])# Interacciones con cada objeto y tipo de interacciones

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)
        
        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")
        
    def analyse_data(self) -> None:
        super().analyse_data()
    
        aux_results = {
            "[NPC_INTERACTION]num_of_interactions": len(self._df),
            "[NPC_INTERACTION]time_btw_interactions": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list())
        }

        for index in range(len(NPCType)):
            aux_results["[NPC_INTERACTION]num_of_interactions_with_actor_{0}".format(index)] = len(self._df[self._df["actor_id"] == index])

        for index in NPCInteractionType:
            aux_results["[NPC_INTERACTION]num_of_interactions_type_{0}".format(index.name)] = len(self._df[self._df["event_type"].str.upper() == index.name])

        self._results.insert_row(aux_results)


    