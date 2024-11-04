import pandas as pd

from models.TablesGroup import TablesGroup
from models.tables.forms import *

class FormTables (TablesGroup):
    '''
    Class FormTables
    ------------------------------

    '''

    _pre_test_df: pd.DataFrame
    _post_test_df: pd.DataFrame

    def __init__(self, user_data):
        super().__init__(user_data)
    # __init__

    def set_data(self) -> None:
        super().set_data()

        self._pre_test_df = self.read_data("meta_responses_1.xlsx")
        self._data["personal_data"] = PersonalDataTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-PD"))
        self._data["pre_test"] = ExamTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-APP"), self._pre_test_df.iloc[0]["Puntuación"])
        self._data["user_experience"] = UserExperienceTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-UX"))
        self._data["usability"] = UsabilityTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-SUS"))
        self._data["cognitive_load"] = CognitiveLoadTable(self._user_data["ID"], self.get_df_by_col_substring(self._pre_test_df, "S-CL"))

        self._post_test_df = self.read_data("meta_responses_2.xlsx")
        self._data["post_test"] = ExamTable(self._user_data["ID"], self.get_df_by_col_substring(self._post_test_df, "S-APP"), self._post_test_df.iloc[0]["Puntuación"])

    def read_data(self, filename) -> None:
        df = pd.read_excel("../data/{0}".format(filename))
        id_col_name = [col for col in df.columns if "[ID]" in col][0]
        return df[df[id_col_name] == self._user_data["ID"]]

    def analyse_data(self) -> None:
        super().analyse_data() 

        self._data["pre_test"].change_results_columns_prefix("EX_PRE_")   
        self._data["post_test"].change_results_columns_prefix("EX_POST_")  
    
    def get_data_from_table(self, table_name):
        return super().get_data_from_table(table_name)
    
    def get_results_df(self) -> pd.DataFrame:
        return super().get_results_df()

    def get_results_dict(self) -> dict:
        return super().get_results_dict()

    def get_result_from_table(self, table_name):
        return super().get_result_from_table(table_name)
    
    def get_result_dict_from_table(self, table_name):
        return super().get_result_dict_from_table(table_name)

    #endregion
        
    #region METODOS PRIVADOS

    def get_df_by_col_substring(self, df, col_subtring) -> pd.DataFrame:
        return df[[col for col in df.columns if col_subtring in col]]

    #endregion
        


    