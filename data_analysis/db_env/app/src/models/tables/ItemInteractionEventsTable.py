import statistics

from models.tables.Table import *
from enums.E_ItemType import ItemType
from enums.E_ItemInteractionType import ItemInteractionType

class ItemInteractionEventsTable(Table):
    '''
    Class ItemInteractionEventsTable
    ------------------------------

    Datos de entrada:
    - id
    - user_id
    - scenario_type
    - actor_id: Actor con el que se hace la interaccion
    - event_type: Tipo de evento
    - event_datetime: Fecha y hora en la que se ha realizado el evento

    Resultados:
    - num_of_interactions: Numero de interacciones con objetos totales
    - time_btw_interactions: Tiempo medio entre cada interaccion
    - num_of_interactions_with_actor_[ITEM_TYPE]: Numero de interacciones con cada tipo de objeto
    - num_of_interactions_type_[ITEM_INTERACTION_TYPE]: Numero de interacciones en base al tipo de interaccion

    '''

    #region VARIABLES PUBLICAS

    _items: pd.DataFrame

    #endregion
    
    #region METODOS PUBLICOS
    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="item_interaction")
        
    # __init__    

    def set_data(self) -> None:
        super().set_data()
        self._items = self.read_data_from_csv("items.csv").set_index('id').reset_index(drop=True)
 
 
    def read_data(self) -> None:
        super().read_data()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")

    # read_data_from_csv


    def analyse_data(self) -> None:
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        super().analyse_df(df)
        #print(df.to_string())
        results = {}

        results["OI_N"] = float(len(df))

        for index in ItemInteractionType:
            results["OI_N_type_{0}".format(index.value)] = float(len(df[df["event_type"].str.upper() == index.name]))

        for index in ItemType:
            results["OI_N_actor_{0}".format(index.value)] = float(len(df[df["actor_id"] == index.value]))
        
        results["OI_T"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        results["OI_T_SS"] = round(np.nanmean(
            [self.get_time_btw_two_type(
                df[(df["hand"] == "Right") & (df["event_type"] == "start_detection")],
                df[(df["hand"] == "Right") & (df["event_type"] == "stop_detection")]),
            self.get_time_btw_two_type(
                df[(df["hand"] == "Left") & (df["event_type"] == "start_detection")],
                df[(df["hand"] == "Left") & (df["event_type"] == "stop_detection")])]), 3)

        results["OI_T_GR"] = round(np.nanmean(
            [self.get_time_btw_two_type(
                df[(df["hand"] == "Right") & (df["event_type"] == "grab")],
                df[(df["hand"] == "Right") & (df["event_type"] == "release")]),
            self.get_time_btw_two_type(
                df[(df["hand"] == "Left") & (df["event_type"] == "grab")],
                df[(df["hand"] == "Left") & (df["event_type"] == "release")])]), 3)

        return results


    def create_graphs(self):
        pass
    
    # analyse_data
        
    #endregion
        
    #region METODOS PRIVADOS

    def get_time_btw_two_type(self, fst_df, snd_df):
        super().get_time_btw_two_type(fst_df, snd_df)

        time_btw = []

        while not fst_df.empty and not snd_df.empty:
            first_event = fst_df.iloc[0]
            snd_event = snd_df.iloc[0]
                
            time = self.get_time_btw_datetimes([first_event["event_datetime"], snd_event["event_datetime"]])
            if time < 0: print("Hay un tiempo entre interacciones de NPC negativo.")

            time_btw.append(time)

            fst_df = fst_df.iloc[1:]
            snd_df = snd_df.iloc[1:]

        if len(time_btw) > 0: return statistics.mean(time_btw)
        else: return np.nan

        '''time_btw = []

        while not fst_df.empty and not snd_df.empty:
            first_event = fst_df.iloc[0]
            
            potential_snd_events = snd_df[(snd_df["scenario_type"] == first_event["scenario_type"]) & (snd_df["actor_name"] == first_event["actor_name"])]
            
            if not potential_snd_events.empty:
                
                snd_event = potential_snd_events.iloc[0]

                time = self.get_time_btw_datetimes([first_event["event_datetime"], snd_event["event_datetime"]])
                if time < 0: print("Hay un tiempo entre interacciones negativo.")

                time_btw.append(time)
                snd_df = snd_df.drop(snd_df[
                    (snd_df["scenario_type"] == first_event["scenario_type"]) & 
                    (snd_df["actor_name"] == first_event["actor_name"])].index[0])
                
                
            else:
                print("PRIMERA HOSTIA", first_event["scenario_type"], first_event["actor_name"])

            fst_df = fst_df.iloc[1:]

        if len(time_btw) > 0: return statistics.mean(time_btw)
        else: return np.nan'''

    #endregion
    