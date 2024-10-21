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

    #endregion
    
    #region METODOS PUBLICOS
    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="item_interaction")
        
    # __init__    

    def set_data(self) -> None:
        super().set_data()

    def read_data_from_csv(self) -> None:
        super().read_data_from_csv()
        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")

    # read_data_from_csv


    def analyse_data(self) -> None:
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        results = {}

        results["OI_NUM"] = float(len(df))

        for index in ItemInteractionType:
            results["OI_NUM_TYPE_{0}".format(index.name)] = float(len(df[df["event_type"].str.upper() == index.name]))

        for index in range(len(ItemType)):
            results["OI_NUM_ACTOR_{0}".format(index)] = float(len(df[df["actor_id"] == index]))
        
        results["OI_TIME_INTER"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        results["OI_TIME_CP_SS"] = round(statistics.mean(
            [self.get_time_btw_two_type_of_inter(
                df[(df["hand"] == "Right") & (df["event_type"] == "start_detection")],
                df[(df["hand"] == "Right") & (df["event_type"] == "stop_detection")]),
            self.get_time_btw_two_type_of_inter(
                df[(df["hand"] == "Left") & (df["event_type"] == "start_detection")],
                df[(df["hand"] == "Left") & (df["event_type"] == "stop_detection")])]), 2)

        results["OI_TIME_CP_GR"] = round(statistics.mean(
            [self.get_time_btw_two_type_of_inter(
                df[(df["hand"] == "Right") & (df["event_type"] == "grab")],
                df[(df["hand"] == "Right") & (df["event_type"] == "release")]),
            self.get_time_btw_two_type_of_inter(
                df[(df["hand"] == "Left") & (df["event_type"] == "grab")],
                df[(df["hand"] == "Left") & (df["event_type"] == "release")])]), 2)

        return results


    def create_graphs(self):
        pass
    
    # analyse_data
        
    #endregion
        
    #region METODOS PRIVADOS

    def get_time_btw_two_type_of_inter(self, first_inter_df, snd_inter_df):

        time_btw = []
        while not first_inter_df.empty and not snd_inter_df.empty:
            time_btw.append(self.get_time_btw_datetimes([first_inter_df.iloc[0]["event_datetime"], snd_inter_df.iloc[0]["event_datetime"]]))
            first_inter_df = first_inter_df.iloc[1:]
            snd_inter_df = snd_inter_df.iloc[1:]

        return statistics.mean(time_btw)

    #endregion
    