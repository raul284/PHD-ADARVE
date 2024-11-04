import pandas as pd

from models.TablesGroup import TablesGroup
from models.tables.events import *

class EventTables(TablesGroup):
    
    def __init__(self, user_data) -> None:
        super().__init__(user_data)

        self._data["gameplay"] = GameplayEventsTable(user_data)
        self._data["item_interaction"] = ItemInteractionEventsTable(user_data)
        #self._data["npc_interaction"] = NPCInteractionEventsTable(user_data)
        #self._data["move"] = MoveEventsTable(user_data)
        #self._data["user_input"] = UserInputEventsTable(user_data)
        #self._data["tutorial_task"] = TutorialTaskEventsTable(user_data)
        #self._data["video"] = VideoEventsTable(user_data)
        '''self._data["place_point"] = PlacePointEventsTable(user_data)
        self._data["help_panel"] = HelpPanelEventsTable(user_data)
        self._data["epd_radiation"] = EPDRadiationEventsTable(user_data)
        self._data["user_radiation"] = UserRadiationEventsTable(user_data)
        self._data["item_radiation"] = ItemRadiationEventsTable(user_data)
        self._data["npc_radiation"] = NPCRadiationEventsTable(user_data)
        self._data["rbq"] = RBQEventsTable(user_data)
        self._data["walkie_report"] = WalkieReportEventsTable(user_data)'''

    def set_data(self) -> None:
        super().set_data()

    def analyse_data(self) -> None:
        super().analyse_data()    
    
    def get_data_from_table(self, table_name):
        return super().get_data_from_table(table_name)
    
    def get_results_df(self) -> pd.DataFrame:
        return super().get_results_df()

    def get_results_dict(self) -> dict:
        return super().get_results_dict()

    def get_result_from_table(self, table_name):
        return super().get_result_from_table(table_name)
    
    def get_result_dict_from_table(self, table_name):
        return super().get_result_dict_from_table(table_name)