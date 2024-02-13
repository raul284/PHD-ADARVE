import os

import pandas as pd

from models.managers.GroupManager import GroupManager

class Group:
    '''
    Class Group
    ----------------
    
    '''
    
    #region VARIABLES PUBLICAS
    
    _users: list

    _manager: GroupManager

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, users):
        self._users = users
        self._manager = GroupManager(self._users)
    
    def set_data(self):
        self._manager.set_data()

    def analyse_data(self):
        self._manager.analyse_data()

    def export_results(self):
        self._manager.export_results()
        

    def create_graphs(self) -> None:
        if not os.path.exists("../results/graphs"):
             os.mkdir("../results/graphs")

        self._manager.create_graphs()

    #region Getters/Setters

    def get_data(self) -> dict:
        return {name: self._manager._tables._data[name]._df for name in self._manager._tables._data}

    def get_data_by_table_name(self, table_name)-> pd.DataFrame:
        return self._manager._tables._data[table_name]._df
    
    #endregion

    #region METODOS PRIVADOS

    #endregion
    
