from models.tables.events import *

class EventTables:
    
    _data: dict


    def __init__(self, user_data) -> None:
        self._data = {}
        #self._data["gameplay"] = GameplayEventsTable(user_data)
        #self._data["item_interaction"] = ItemInteractionEventsTable(user_data)
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
        for table in self._data:
            assert self._data[table] != None, "La tabla <<{0}>> no tiene valor".format(table)
            self._data[table].set_data()


    def analyse_data(self) -> None:
        for table in self._data:
            self._data[table].analyse_data()        

    def get_data_from_table(self, table_name):
        return self._data[table_name]._df

    def get_result_from_table(self, table_name):
        return self._data[table_name]._results._df
    
    def get_result_dict_from_table(self, table_name):
        return self.get_result_from_table(table_name=table_name).to_dict()
    
    def get_result_value_from_table(self, table_name, key):
        return self.get_result_dict_from_table(table_name=table_name)[key][0]