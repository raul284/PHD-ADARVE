from dataclasses import dataclass

from models.tables import *

@dataclass
class TablesList:
    
    _data: dict

    def __init__(self) -> None:
        self._data = {}
        #self._data["form_marks"] = FormTable("form", sheet_names=["personal_data", "exam", "sus"])
        self._data["gameplay_events"] = GameplayEventsTable("gameplay")
        self._data["item_interaction_events"] = ItemInteractionEventsTable("item_interaction")
        self._data["npc_interaction_events"] = NPCInteractionEventsTable("npc_interaction")
        self._data["move_events"] = MoveEventsTable("move")
        #self._data["place_point_events"] = PlacePointEventsTable(PlacePointEvent)
        #self._data["tips_events"] = TipsEventsTable(tips_ingame_enabled=tips_ingame_enabled)
        self._data["user_input_events"] = UserInputEventsTable("user_inputs")

    def get_data_from_table(self, table_name):
        return self._data[table_name]._df

    def get_result_from_table(self, table_name):
        return self._data[table_name]._results._df
    
    def get_result_dict_from_table(self, table_name):
        return self.get_result_from_table(table_name=table_name).to_dict()
    
    def get_result_value_from_table(self, table_name, key):
        return self.get_result_dict_from_table(table_name=table_name)[key][0]