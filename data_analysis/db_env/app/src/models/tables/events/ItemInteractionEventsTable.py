import statistics

from models.tables.events.Table import *
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
        self._items = self._items.replace("T1_BasicMechanics", "T1").replace("S1_BasicMechanics", "S1").replace("T2_BasicEmergency", "T2").replace("S2_BasicEmergency", "S2")
 
 
    def read_data(self) -> None:
        super().read_data()
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")

    # read_data_from_csv


    def analyse_data(self) -> None:
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        return super().analyse_df(df)
        #print(df.to_string())

    def analyse_number(self, df):
        results = {}
        aux_items = self._items[self._items["scenario_type"].isin(df["scenario_type"].unique())]

        # Número de interacciones
        results["OI_N"] = float(len(df))
        # Número de interacciones con la mano DERECHA
        results["OI_N_R"] = float(len(df[(df["hand"] == "Right")]))
        # Número de interacciones con la mano IZQUIERDA 
        results["OI_N_L"] = float(len(df[(df["hand"] == "Left")]))

        # Número de interacciones en base al tipo de interacción
        for index in ItemInteractionType:
            results["OI_N_t_{0}".format(index.value)] = float(len(df[df["event_type"].str.upper() == index.name]))
            # Número de interacciones en base al tipo de interacción con la mano DERECHA
            results["OI_N_t_{0}_R".format(index.value)] = float(len(df[(df["hand"] == "Right") & (df["event_type"].str.upper() == index.name)]))
            # Número de interacciones en base al tipo de interacción con la mano IZQUIERDA
            results["OI_N_t_{0}_L".format(index.value)] = float(len(df[(df["hand"] == "Left") & (df["event_type"].str.upper() == index.name)]))

        # Número de interacciones en base al tipo de objeto
        for index in ItemType:
            if self.actor_is_in_scenario(index.value, aux_items):
                results["OI_N_a_{0}".format(index.value)] = float(len(df[df["actor_id"] == index.value]))
            else: results["OI_N_a_{0}".format(index.value)] = np.nan
        
        return results
    
    def analyse_time(self, df):
        results = {}
        aux_items = self._items[self._items["scenario_type"].isin(df["scenario_type"].unique())]

        # Tiempo entre interacciones
        results["OI_T"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())
        # Tiempo entre interacciones con la mano DERECHA
        results["OI_T_R"] = self.get_time_btw_datetimes(df[df["hand"] == "Right"]["event_datetime"].to_list())
        # Tiempo entre interacciones con la mano IZQUIERDA
        results["OI_T_L"] = self.get_time_btw_datetimes(df[df["hand"] == "Left"]["event_datetime"].to_list())

        # Tiempo entre interacciones START y STOP DETECTION
        right = self.get_time_btw_two_type(
                df[(df["hand"] == "Right") & (df["event_type"] == "start_detection")],
                df[(df["hand"] == "Right") & (df["event_type"] == "stop_detection")], ["scenario_type", "actor_name"])
        left = self.get_time_btw_two_type(
                df[(df["hand"] == "Left") & (df["event_type"] == "start_detection")],
                df[(df["hand"] == "Left") & (df["event_type"] == "stop_detection")], ["scenario_type", "actor_name"])
        
        results["OI_T_SS"] = round(np.nanmean([right, left]), 3)
        # Tiempo entre interacciones START y STOP DETECTION con la mano DERECHA
        results["OI_T_SS_R"] = right
        # Tiempo entre interacciones START y STOP DETECTION con la mano IZQUIERDA
        results["OI_T_SS_L"] = left

        # Tiempo entre interacciones GRAB y RELEASE
        right = self.get_time_btw_two_type(
                df[(df["hand"] == "Right") & (df["event_type"] == "grab")],
                df[(df["hand"] == "Right") & (df["event_type"] == "release")], ["scenario_type", "actor_name"])
        left = self.get_time_btw_two_type(
                df[(df["hand"] == "Left") & (df["event_type"] == "grab")],
                df[(df["hand"] == "Left") & (df["event_type"] == "release")], ["scenario_type", "actor_name"])

        results["OI_T_GR"] = round(np.nanmean([right, left]), 3)
        # Tiempo entre interacciones GRAB y RELEASE con la mano DERECHA
        results["OI_T_GR_R"] = right
        # Tiempo entre interacciones GRAB y RELEASE con la mano IZQUIERDA
        results["OI_T_GR_L"] = left

        for index in ItemType:
            if self.actor_is_in_scenario(index.value, aux_items):

                right = self.get_time_btw_two_type(
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Right") & (df["event_type"] == "start_detection")],
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Right") & (df["event_type"] == "stop_detection")], ["scenario_type", "actor_name"])
                left = self.get_time_btw_two_type(
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Left") & (df["event_type"] == "start_detection")],
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Left") & (df["event_type"] == "stop_detection")], ["scenario_type", "actor_name"])
    
                results["OI_T_SS_a_{0}".format(index.value)] = round(np.nanmean([right, left]), 3)

            else: 
                results["OI_T_SS_a_{0}".format(index.value)] = np.nan

        for index in ItemType:
            if self.actor_is_in_scenario(index.value, aux_items):     

                right = self.get_time_btw_two_type(
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Right") & (df["event_type"] == "grab")],
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Right") & (df["event_type"] == "release")], ["scenario_type", "actor_name"])
                left = self.get_time_btw_two_type(
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Left") & (df["event_type"] == "grab")],
                        df[(df["actor_id"] == index.value) & (df["hand"] == "Left") & (df["event_type"] == "release")], ["scenario_type", "actor_name"])
                results["OI_T_GR_a_{0}".format(index.value)] = round(np.nanmean([right, left]), 3)

            else: 
                results["OI_T_GR_a_{0}".format(index.value)] = np.nan

        return results


    def create_graphs(self):
        pass
    
    # analyse_data
        
    #endregion
        
    #region METODOS PRIVADOS

    def actor_is_in_scenario(self, actor_id, df):
        return actor_id in df["actor_id"].unique()

    #endregion
    