import os

import pandas as pd
from datetime import datetime

from models.FormTables import FormTables
from models.EventTables import EventTables
from models.CombinedTable import CombinedTable

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

    _form_tables: FormTables
    _event_tables: EventTables
    _combined_table: CombinedTable


    #_manager: UserManager

    _results_path: str
    _results: pd.DataFrame

    #endregion

    #region METODOS PUBLICOS

    def __init__(self, id:str = "", experiment_id:str = "", group:str = "", hmd:str = "", event_datetime:str = ""):
        self._id = id
        self._experiment_id = experiment_id
        self._group = group
        self._hmd = hmd
        self._date_created = datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S.%f')

        self._user_data = {"ID": self._id, "EXP_ID": self._experiment_id, "GROUP": self._group, "HMD": self._hmd}

        self._result_path = "../results/{0}/".format(self._id)
        self._results = pd.DataFrame()

    def __repr__(self):
        return f'User({self._id}, {self._group}, {self._hmd})'

    def __str__(self):
        return f'User({self._id}, {self._group}, {self._hmd})'
    
    def set_data(self):
        self._form_tables = FormTables(self._user_data)
        self._form_tables.set_data()

        self._event_tables = EventTables(self._user_data)
        self._event_tables.set_data()

        self._combined_table = CombinedTable(self._user_data)
        self._combined_table.set_data(self._event_tables)

    def analyse_data(self):
        self._form_tables.analyse_data()
        self._event_tables.analyse_data()
        self._combined_table.analyse_data()

        form_results = self._form_tables.get_results_df()
        event_results = self._event_tables.get_results_df()
        combined_results = self._combined_table.get_results_df()

        form_results = pd.concat([form_results] * len(event_results), axis=0).reset_index(drop=True)
        self._results = pd.concat([form_results, event_results], axis=1).reset_index(drop=True)
        self._results = self._results.loc[:, ~self._results.columns.duplicated()]

    def export_results(self):
        if not os.path.exists(self._result_path):
            os.makedirs(self._result_path)

    def create_graphs(self) -> None:
        pass

    #endregion

    #region Getters/Setters
            
    def get_results(self) -> pd.DataFrame:  
        return self._results

    def get_results_by_table_name(self, df, table_name) -> pd.DataFrame:
        return df._data[table_name].get_results()
    
    #endregion

    #region METODOS PRIVADOS

    #endregion