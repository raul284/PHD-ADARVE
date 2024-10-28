from models.tables import *

class UserTables:
    
    _data: dict

    def __init__(self, user_data) -> None:
        self._data = {}
        print("CLARO QUE TENGO TABLA")
        #self._data["form_marks"] = FormTable("form", sheet_names=["personal_data", "exam", "sus"])
        #self._data["gameplay_events"] = GameplayEventsTable(user_data)
        #self._data["item_interaction_events"] = ItemInteractionEventsTable(user_data)
        #self._data["npc_interaction_events"] = NPCInteractionEventsTable(user_data)
        #self._data["move_events"] = MoveEventsTable(user_data)
        self._data["user_input_events"] = UserInputEventsTable(user_data)
        '''self._data["place_point_events"] = PlacePointEventsTable(user_data)
        self._data["user_input_events"] = UserInputEventsTable(user_data)
        self._data["help_panel_events"] = HelpPanelEventsTable(user_data)
        self._data["epd_radiation_events"] = EPDRadiationEventsTable(user_data)
        self._data["user_radiation_events"] = UserRadiationEventsTable(user_data)
        self._data["item_radiation_events"] = ItemRadiationEventsTable(user_data)
        self._data["npc_radiation_events"] = NPCRadiationEventsTable(user_data)
        self._data["rbq_events"] = RBQEventsTable(user_data)
        self._data["tutorial_task_events"] = TutorialTaskEventsTable(user_data)
        self._data["video_events"] = VideoEventsTable(user_data)
        self._data["walkie_report_events"] = WalkieReportEventsTable(user_data)'''

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