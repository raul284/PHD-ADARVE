import os

import pandas as pd
from datetime import datetime

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
    _group: str
    _created: datetime

    _main_data_df: pd.DataFrame

    _manager: UserManager

    _results_path: str

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, id:int = 0, user_name:str = "", user_group:str = "", event_datetime:str = ""):
        self._id = id
        self._user_name = user_name
        self._group = user_group
        self._created = datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S.%f')

        self._main_data_df = pd.DataFrame({"ID": [self._user_name], "GROUP": [self._group]})

        self._manager = UserManager()

        self._result_path = "../results/{0}/".format(self._id)

    def __repr__(self):
        return f'User({self._id}, {self._user_name})'

    def __str__(self):
        return f'User({self._id}, {self._user_name})'
    
    def set_data(self, tables):
        self._manager.set_data(tables)

    def analyse_data(self):
        self._manager.analyse_data()

    def export_results(self):
        if not os.path.exists(self._result_path):
            os.makedirs(self._result_path)
        self._manager.export_results()

    def create_graphs(self) -> None:
        self._manager.create_graphs(self._result_path)

    #endregion

    #region Getters/Setters
        
    def add_form_data(self, form) -> None:
        self._manager.add_form_data(self._user_name, form)

    def get_data(self) -> dict:
        return {name: self._manager._data._tables._data[name]._df for name in self._manager._data._tables._data}

    def get_data_by_table_name(self, table_name)-> pd.DataFrame:
        return self._manager._data._tables._data[table_name]._df
    
    def get_results(self) -> pd.DataFrame:
        pass
        #return pd.concat([self._main_data_df, self._manager._results, self._manager._combined_results._results._df], axis=1)

    def get_results_by_table_name(self, table_name) -> pd.DataFrame:
        return self._manager._results._tables._data[table_name]._results._df
    
    #endregion

    #region METODOS PRIVADOS

    #endregion