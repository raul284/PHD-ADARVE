import pandas as pd
import matplotlib.pyplot as plt

from models.tables import *
from structs.F_TablesList import TablesList

class UserManager:
    '''
    Class UserManager
    ------------------------------
    
    '''

    #region VARIABLES PUBLICAS

    _data: pd.DataFrame
    _results: pd.DataFrame

    _tables: TablesList
    _combined_results: CombinedEventsTable

    #endregion


    #region METODOS PUBLICOS

    def __init__(self) -> None:
        self._data = pd.DataFrame()
        self._results = pd.DataFrame()
        
        self._tables = TablesList()
        #self._combined_results = CombinedEventsTable()

    def set_data(self, tables) -> None:
        for table_name in tables:
            self.set_table_dataframe(table_name, tables[table_name])

        #self._results.set_data(tables)

    def analyse_data(self) -> None:
        for table_name in self._tables._data:
            if table_name is not "combined_events":
                self._tables._data[table_name].analyse_data()
            else:
                self._tables._data[table_name].analyse_data(self._tables)

            self._results = pd.concat([self._results, self._tables._data[table_name].get_results()], axis=1) 

        #self._combined_results.analyse_data(self._tables)
         

    def export_results(self) -> None:
        pass

    def create_graphs(self, path) -> None:
        x_lim = (self._tables._data["gameplay_events"]._start_time, self._tables._data["gameplay_events"]._end_time)

        chart_index = 0
        for table in self._tables._data:
            self._tables._data[table].create_graphs(path, x_lim)
            #axs[chart_index].set_xlim(left=x_lim[0], right=x_lim[1])

            chart_index += 1

        #plt.show()


    #endregion

    #region Getters/Setters

    def add_form_data(self, user_name, form):
        form_dict = form.get_data_by_user(user_name=user_name)
        self._personal_data_df = form_dict["personal_data"]

    def get_table_list_data(self) -> dict:
        return self._tables._data

    def set_table_dataframe(self, table_name, new_df) -> None:
        self.get_table_list_data()[table_name]._df = new_df

    def get_table_dataframe(self, table_name) -> pd.DataFrame:
        return self.get_table_list_data()[table_name]._df

    #endregion
    
    #region METODOS PRIVADOS

    #endregion