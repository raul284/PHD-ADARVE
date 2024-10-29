from models.tables.forms import *
from enums.E_GenreType import GenreType


class FormTables:
    '''
    Class FormTables
    ------------------------------

    '''
    _data: dict

    def __init__(self, user_data) -> None:
        self._data = {}
        self._data["pre_test"] = Table(user_data, "pre_test")

    # __init__

    def set_data(self) -> None:
        self._data["pre_test"].set_data("meta_responses_1.xlsx")

    def analyse_data(self) -> None:
        for table in self._data:
            self._data[table].analyse_data()  

    def get_data_from_table(self, table_name):
        return self._data[table_name]._df

    def get_result_from_table(self, table_name):
        return self._data[table_name]._results._df

    #endregion
        
    #region METODOS PRIVADOS

    #endregion
        


    