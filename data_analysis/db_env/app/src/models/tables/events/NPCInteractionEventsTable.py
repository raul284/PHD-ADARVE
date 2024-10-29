from enums.E_NPCType import NPCType
from enums.E_NPCInteractionType import NPCInteractionType

from models.tables.events.Table import *

class NPCInteractionEventsTable(Table):
    
    #region VARIABLES PUBLICAS

    _npcs: pd.DataFrame

    #endregion
    
    #region METODOS PUBLICOS
    def __init__(self, user_data) -> None:
        super().__init__(user_data=user_data, table_name="npc_interaction")

    def set_data(self) -> None:
        super().set_data()
        self._npcs = self.read_data_from_csv("npcs.csv").set_index('id').reset_index(drop=True)

    def read_data(self) -> None:
        super().read_data()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        
    def analyse_data(self) -> None:
        super().analyse_data()
    
    def analyse_df(self, df) -> dict:
        return super().analyse_df(df)
        #print(df.to_string())

    def analyse_number(self, df):
        results = {}

        #print(df.to_string())

        results["NPC_N"] = float(len(df))

        for index in NPCInteractionType:
            results["NPC_N_type_{0}".format(index.value)] = float(len(df[df["event_type"].str.upper() == index.name]))

        for index in NPCType:
            results["NPC_N_actor_{0}".format(index.value)] = float(len(df[df["actor_id"] == index.value]))

        return results

    def analyse_time(self, df) -> dict:
        results = {}
        # Aqui hay que hacer una distincion de tiempo entre interacciones
        results["NPC_T"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        # Tiempo entre el start y el stop conversationes. Con esto se deberia ver si alguien se la salta.
        for npc_id in pd.unique(df["actor_id"]):
            results["NPC_T_SS"] = self.get_time_btw_two_type(
                df[df["event_type"] == "start_talk_with_npc"],
                df[df["event_type"] == "stop_talk_with_npc"], ["actor_id"])


        # Tiempo entre conversaciones. Independiente del NPC
        df_c = pd.DataFrame()
        for scenario in pd.unique(df["scenario_type"]):
            aux_df = df[df["scenario_type"] == scenario]
            aux_df = aux_df.drop(aux_df.tail(1).index)
            aux_df = aux_df.drop(aux_df.head(1).index)
            if not aux_df.empty: df_c = pd.concat([df_c, aux_df])

        if not df_c.empty:
            results["NPC_T_C"] = self.get_time_btw_two_type(
                df_c[(df_c["event_type"] == "stop_talk_with_npc")],
                df_c[(df_c["event_type"] == "start_talk_with_npc")], [])
        else: results["NPC_T_C"] = np.nan

        return results

    def create_graphs(self):
        pass

    '''def get_time_btw_two_type(self, fst_df, snd_df):
        #super().get_time_btw_two_type(fst_df, snd_df)

        time_btw = []

        while not fst_df.empty and not snd_df.empty:
            first_event = fst_df.iloc[0]
            snd_event = snd_df.iloc[0]

            print(fst_df)
            print(snd_df)
                
            time = self.get_time_btw_datetimes([first_event["event_datetime"], snd_event["event_datetime"]])
            if time < 0: print("Hay un tiempo entre interacciones de NPC negativo.")

            time_btw.append(time)

            fst_df = fst_df.iloc[1:]
            snd_df = snd_df.iloc[1:]

        if len(time_btw) > 0: return statistics.mean(time_btw)
        else: return np.nan'''

    #endregion

    