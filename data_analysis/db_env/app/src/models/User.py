import os

import pandas as pd

from enums.E_GroupType import GroupType
from models.managers.UserManager import UserManager

class User:
    '''
    Class User
    --------------------

    '''
    
    #region VARIABLES PUBLICAS

    _id: int
    _user_name: str
    _tips_ingame_enabled: bool

    _main_data_df: pd.DataFrame

    _manager: UserManager

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, id:int = 0, user_name:str = "", tips_ingame_enabled:str = ""):
        self._id = id
        self._user_name = user_name
        self._tips_ingame_enabled = tips_ingame_enabled

        self._main_data_df = pd.DataFrame({"ID": [self._user_name], "GROUP": [GroupType.G_VR.name if self._tips_ingame_enabled else GroupType.G_TRA.name]})

        self._manager = UserManager()

    def __repr__(self):
        return f'User({self._id}, {self._user_name})'

    def __str__(self):
        return f'User({self._id}, {self._user_name})'
    
    def set_data(self, tables):
        self._manager.set_data(tables)

    def analyse_data(self):
        self._manager.analyse_data()

    def export_results(self):
        self._manager.export_results()

    def create_graphs(self) -> None:
        self._manager.create_graphs()

    #endregion

    #region Getters/Setters
        
    def add_form_data(self, form) -> None:
        self._manager.add_form_data(self._user_name, form)

    def get_data(self) -> dict:
        return {name: self._manager._data._tables._data[name]._df for name in self._manager._data._tables._data}

    def get_data_by_table_name(self, table_name)-> pd.DataFrame:
        return self._manager._data._tables._data[table_name]._df
    
    def get_results(self) -> pd.DataFrame:
        return pd.concat([self._main_data_df, self._manager._results, self._manager._combined_results._results._df], axis=1)

    def get_results_by_table_name(self, table_name) -> pd.DataFrame:
        return self._manager._results._tables._data[table_name]._results._df
    
    #endregion

    #region METODOS PRIVADOS

    #endregion