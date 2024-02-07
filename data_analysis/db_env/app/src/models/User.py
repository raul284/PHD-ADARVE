import os

from managers.DataManager import DataManager
from models.tables.ResultsTable import ResultsTable

class User:
    _id: int
    _user_name: str
    _tips_ingame_enabled: bool

    _data_manager: dict

    def __init__(self, id:int = 0, user_name:str = "", tips_ingame_enabled:str = ""):
        self._id = id
        self._user_name = user_name
        self._tips_ingame_enabled = tips_ingame_enabled
        self._data_manager = DataManager(self._tips_ingame_enabled)

    def __repr__(self):
        return f'User({self._id}, {self._user_name})'

    def __str__(self):
        return f'User({self._id}, {self._user_name})'
    
    def set_data(self):
        self._data_manager.set_data()

    def analyse_data(self):
        self._data_manager.analyse_data()

    def get_results(self):
        return self._data_manager.get_results()

    def get_joined_results(self):
        return self._data_manager.get_joined_results()

    def export_results(self):
        results_dir = "../results/{0}".format(self._id)
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)

        self._data_manager.export_results()

    def create_graphs(self) -> None:
        self._data_manager.create_graphs()