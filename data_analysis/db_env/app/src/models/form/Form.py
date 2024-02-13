import pandas as pd

class Form:
    '''
    Class Form
    --------------
    '''

    #region VARIABLES PUBLICAS

    _personal_data_df: pd.DataFrame
    _exam_df: pd.DataFrame
    _sus_df: pd.DataFrame

    #endregion

    #region METODOS PUBLICOS

    def __init__(self):
        pass

    def set_data(self, filename) -> None:
        self._personal_data_df = pd.read_excel("../data/{0}.xlsx".format(filename), sheet_name="personal_data")
        self._exam_df = pd.read_excel("../data/{0}.xlsx".format(filename), sheet_name="exam")
        self._sus_df = pd.read_excel("../data/{0}.xlsx".format(filename), sheet_name="sus")

    def analyse_data(self) -> None:
        pass

    def export_results(self) -> None:
        pass

    def create_graphs(self) -> None:
        pass

    #endregion

    #region Getters/Setters
    
    def get_data_by_user(self, user_name) -> dict:
        return {"personal_data": self._personal_data_df[self._personal_data_df["id"] == user_name],
                "exam": self._exam_df[self._exam_df["id"] == user_name],
                "sus": self._sus_df[self._sus_df["id"] == user_name]}

    #endregion

    #region METODOS PRIVADOS

    #endregion

        

    








