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
    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)

        self._results = ResultsTable(["OI_NUM"] + \
                ["OI_NUM_ACTOR_{0}".format(index) for index in range(len(ItemType))] + \
                    ["OI_NUM_TYPE_{0}".format(index.name) for index in ItemInteractionType] + \
                    ["OI_TIME_INTER", "OI_TIME_CP"])
        
    # __init__    


    def read_data_from_csv(self, filename: str) -> None:

        super().read_data_from_csv(filename)
      
        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S")

    # read_data_from_csv


    def analyse_data(self) -> None:
    
        super().analyse_data()

        aux_results = {
            "OI_NUM": float(len(self._df)),
            "OI_NUM_GP_STEPS": 0.0,
            "OI_TIME_INTER": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list()),
            "OI_TIME_CP": 0.0
        }

        for index in range(len(ItemType)):
            aux_results["OI_NUM_ACTOR_{0}".format(index)] = float(len(self._df[self._df["actor_id"] == index]))

        for index in ItemInteractionType:
            aux_results["OI_NUM_TYPE_{0}".format(index.name)] = float(len(self._df[self._df["event_type"].str.upper() == index.name]))

        self._results.insert_row(aux_results)
    
    # analyse_data
        
    #endregion
        
    #region METODOS PRIVADOS

    #endregion
    