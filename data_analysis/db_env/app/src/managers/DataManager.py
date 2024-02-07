import pandas as pd

from models.events import *
from models.tables import *

class DataManager:
    '''
    Class DataManager
    --------------------------

    '''

    #region VARIABLES PUBLICAS

    _tables: dict

    _tips_ingame_enabled: bool

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, tips_ingame_enabled) -> None:
        self._tables = {}
        self._tips_ingame_enabled = tips_ingame_enabled

    def set_data(self) -> None:
        self._tables["gameplay_events"] = GameplayEventsTable(GameplayEvent)
        self._tables["item_interaction_events"] = ItemInteractionEventsTable(ItemInteractionEvent)
        self._tables["npc_interaction_events"] = NPCInteractionEventsTable(NPCInteractionEvent)
        self._tables["move_events"] = MoveEventsTable(MoveEvent)
        #self._tables["place_point_events"] = PlacePointEventsTable(PlacePointEvent)
        self._tables["tips_events"] = TipsEventsTable(TipsEvent, tips_ingame_enabled=self._tips_ingame_enabled)
        self._tables["user_input_events"] = UserInputEventsTable(UserInputEvent)

    def analyse_data(self) -> None:
        for key in self._tables:
            self._tables[key].analyse_data()

    def get_results(self) -> list:
        return {key : self._tables[key].get_results() for key in self._tables}

    def get_joined_results(self) -> None:
        pass

    def export_results(self) -> None:
        pass

    def create_graphs(self) -> None:
        for key in self._tables:
            self._tables[key].create_graphs()

    def get_joined_results(self) -> pd.DataFrame:
        print(self._tables["gameplay_events"]._results._df)
        aux_list = [self._tables[key]._results._df for key in self._tables]
        return pd.concat(aux_list)

    #endregion

    #region METODOS PRIVADOS

    #endregion