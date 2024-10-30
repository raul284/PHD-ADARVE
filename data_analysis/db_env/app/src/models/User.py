import os

import pandas as pd
from datetime import datetime

from models.EventTables import EventTables
from models.FormTables import FormTables

class User:
    '''
    Class User
    --------------------

    '''
    
    #region VARIABLES PUBLICAS

    _id: str
    _experiment_id: str
    _group: str
    _hmd: str
    _date_created: datetime

    _main_data: dict

    _event_tables: EventTables
    _form_tables: FormTables

    #_manager: UserManager

    _results_path: str

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, id:str = "", experiment_id:str = "", group:str = "", hmd:str = "", event_datetime:str = ""):
        self._id = id
        self._experiment_id = experiment_id
        self._group = group
        self._hmd = hmd
        self._date_created = datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S.%f')

        self._main_data = {"ID": self._id, "EXP_ID": self._experiment_id, "GROUP": self._group, "HMD": self._hmd}

        self._result_path = "../results/{0}/".format(self._id)

    def __repr__(self):
        return f'User({self._id}, {self._group}, {self._hmd})'

    def __str__(self):
        return f'User({self._id}, {self._group}, {self._hmd})'
    
    def set_data(self):
        self._event_tables = EventTables(self._main_data)
        self._event_tables.set_data()

        self._form_tables = FormTables(self._main_data)
        self._form_tables.set_data()

    def analyse_data(self):
        self._event_tables.analyse_data()
        self._form_tables.analyse_data()

    def export_results(self):
        if not os.path.exists(self._result_path):
            os.makedirs(self._result_path)

    def create_graphs(self) -> None:
        pass

    #endregion

    #region Getters/Setters
            
    def get_results(self) -> dict:  
        return {
            "APP": self.get_event_results(),
            "FORM": self.get_form_results()
        }

    def get_event_results(self) -> dict:      
        return {table: self.get_results_by_table_name(self._event_tables, table) for table in self._event_tables._data}
    
    def get_form_results(self) -> dict:      
        return {table: self.get_results_by_table_name(self._form_tables, table) for table in self._form_tables._data}


    def get_results_by_table_name(self, df, table_name) -> pd.DataFrame:
        return df._data[table_name].get_results()
    
    #endregion

    #region METODOS PRIVADOS

    #endregion