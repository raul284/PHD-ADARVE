import pandas as pd

from models.tables.forms import *

class FormTables:
    '''
    Class FormTables
    ------------------------------

    '''
    _data: dict
    _user_data: dict

    _pre_test_df: pd.DataFrame
    _post_test_df: pd.DataFrame

    def __init__(self, user_data) -> None:
        self._data = {}
        self._user_data = user_data
    # __init__

    def set_data(self) -> None:
        self._pre_test_df = self.read_data("meta_responses_1.xlsx")
        self._data["personal_data"] = PersonalDataTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-PD"))
        self._data["user_experience"] = UserExperienceTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-UX"))
        self._data["usability"] = UsabilityTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-SUS"))
        self._data["cognitive_load"] = CognitiveLoadTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-CL"))
        #self._data["pre_test"] = PersonalDataTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-APP"))

        #self._post_test_df = self.read_data("meta_responses_2.xlsx")
        #self._data["post_test"] = PersonalDataTable(self._user_data["ID"], self.get_df_by_col_substring(self._post_test_df, "S-APP"))

    def read_data(self, filename) -> None:
        df = pd.read_excel("../data/{0}".format(filename))
        id_col_name = [col for col in df.columns if "[ID]" in col][0]
        return df[df[id_col_name] == self._user_data["ID"]]

    def analyse_data(self) -> None:
        for table in self._data:
            self._data[table].analyse_data()  

    def get_data_from_table(self, table_name):
        return self._data[table_name]._df

    def get_results_from_table(self, table_name) -> pd.DataFrame:
        return self._data[table_name].get_results()

    #endregion
        
    #region METODOS PRIVADOS

    def get_df_by_col_substring(self, df, col_subtring) -> pd.DataFrame:
        return df[[col for col in df.columns if col_subtring in col]]

    #endregion
        


    