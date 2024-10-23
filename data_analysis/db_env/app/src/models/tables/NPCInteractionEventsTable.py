from enums.E_NPCType import NPCType
from enums.E_NPCInteractionType import NPCInteractionType

from models.tables.Table import *

class NPCInteractionEventsTable(Table):
    
    def __init__(self, user_data) -> None:
        super().__init__(user_data=user_data, table_name="npc_interaction")

    def read_data_from_csv(self) -> None:
        super().read_data_from_csv()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        
    def analyse_data(self) -> None:
        super().analyse_data()
    
    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        results = {}

        #print(df.to_string())

        results["NPC_N"] = float(len(df))
        # Aqui hay que hacer una distincion de tiempo entre interacciones
        results["NPC_T"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        for index in NPCInteractionType:
            results["NPC_N_type_{0}".format(index.value)] = float(len(df[df["event_type"].str.upper() == index.name]))

        for index in NPCType:
            results["NPC_N_actor_{0}".format(index.value)] = float(len(df[df["actor_id"] == index.value]))

        return results

    def create_graphs(self):
        pass


    