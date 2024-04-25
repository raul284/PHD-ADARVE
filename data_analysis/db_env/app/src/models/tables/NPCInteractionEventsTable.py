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
        
        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        
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

    def create_graphs(self, path, lims):
        super().create_graphs(path, lims)

    def create_graphs_for_eeg(self, path, lims):
        super().create_graphs_for_eeg(path, lims)
        
        aux_df = self._df[["actor_id", "event_type", "event_datetime"]]
        print(self._df)

        fig, axs = plt.subplots(len(aux_df["actor_id"].drop_duplicates()) + 1, 1, figsize=(14, 6), layout='tight', sharex=True)

        axis_index = 0
        for event in aux_df["actor_id"].drop_duplicates():
            aux_df[(aux_df["actor_id"] == event) & (aux_df["event_type"] == "start_talk_with_npc")].plot.scatter(x='event_datetime', y="actor_id", c="blue", ax=axs[axis_index])
            aux_df[(aux_df["actor_id"] == event) & (aux_df["event_type"] == "stop_talk_with_npc")].plot.scatter(x='event_datetime', y="actor_id", c="red", ax= axs[axis_index])
            
            axs[axis_index].set_xlim(left=lims[0], right=lims[1])
            axs[axis_index].set_ylabel("")

            axis_index += 1

        plt.xlabel("Time")

        plt.savefig("{0}npc_interaction_eeg".format(path))


    