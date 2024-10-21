import os

import pandas as pd
from datetime import datetime

from models.UserTables import UserTables

class User:
    '''
    Class User
    --------------------

    '''
    
    #region VARIABLES PUBLICAS

    _id: str
    _group: str
    _hmd: str
    _date_created: datetime

    _main_data: dict

    _tables: UserTables

    #_manager: UserManager

    _results_path: str

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, id:str = "", group:str = "", hmd:str = "", event_datetime:str = ""):
        self._id = id
        self._group = group
        self._hmd = hmd
        self._date_created = datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S.%f')

        self._main_data = {"ID": self._id, "GROUP": self._group, "HMD": self._hmd}

        #self._manager = UserManager()

        self._result_path = "../results/{0}/".format(self._id)

    def __repr__(self):
        return f'User({self._id}, {self._group}, {self._hmd})'

    def __str__(self):
        return f'User({self._id}, {self._group}, {self._hmd})'
    
    def set_data(self):
        self._tables = UserTables(self._main_data)
        self._tables.set_data()

    def analyse_data(self):
        self._tables.analyse_data()

    def export_results(self):
        if not os.path.exists(self._result_path):
            os.makedirs(self._result_path)
        self._manager.export_results()

    def create_graphs(self) -> None:
        self._manager.create_graphs(self._result_path)

    #endregion

    #region Getters/Setters
        
    def add_form_data(self, form) -> None:
        self._manager.add_form_data(self._id, form)

    def get_data(self) -> dict:
        return {name: self._manager._data._tables._data[name]._df for name in self._manager._data._tables._data}

    def get_data_by_table_name(self, table_name)-> pd.DataFrame:
        return self._manager._data._tables._data[table_name]._df
    
    def get_results(self) -> pd.DataFrame:        
        return {table: self.get_results_by_table_name(table) for table in self._tables._data}

    def get_results_by_table_name(self, table_name) -> pd.DataFrame:
        return self._tables._data[table_name].get_results()
    
    #endregion

    #region METODOS PRIVADOS

    #endregion