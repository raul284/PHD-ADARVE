import pandas as pd

from models.tables.events import *

class TablesGroup:
    
    _data: dict
    _user_data: dict

    def __init__(self, user_data) -> None:
        self._data = {}
        self._user_data = user_data


    def set_data(self) -> None:
        for table in self._data:
            assert self._data[table] != None, "La tabla <<{0}>> no tiene valor".format(table)
            self._data[table].set_data()


    def analyse_data(self) -> None:
        for table in self._data:
            self._data[table].analyse_data()     

    def get_results_df(self) -> pd.DataFrame:
        result = pd.DataFrame()
        for table in self._data:
            result = pd.concat([result, self.get_result_from_table(table)], axis=1) 
        return result.loc[:, ~result.columns.duplicated()]

    def get_results_dict(self) -> dict:
        results = {}
        
        for table in self._data:
            results[table] = self._data[table].get_results()

        return results

    def get_data_from_table(self, table_name):
        return self._data[table_name]._df

    def get_result_from_table(self, table_name) -> pd.DataFrame:
        return self._data[table_name].get_results()
    
    def get_result_dict_from_table(self, table_name) -> dict:
        return self.get_result_from_table(table_name=table_name).to_dict()