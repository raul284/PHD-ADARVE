from models.tables.Table import *

from enums.E_GenreType import GenreType


class FormTable(Table):
    '''
    Class FormTable
    ------------------------------

    '''

    #region VARIABLES PUBLICAS

    _sheet_names: list

    #endregion
    
    #region METODOS PUBLICOS

    def __init__(self, table_name:str="", sheet_names:list = []) -> None:

        super().__init__(table_name=table_name)

        self._sheet_names = sheet_names

        self._results = ResultsTable([""])

    # __init__

    def read_data_from_csv(self, filename:str="") -> None:
        #self._df = pd.read_excel("../data/{0}.xlsx".format(filename))
        self._df = pd.DataFrame()
        
        for name in self._sheet_names:
            
            sheet_df = pd.read_excel("../data/{0}.xlsx".format(filename), sheet_name=name)
            sheet_df = self.rename_sheets_cols(sheet_df, name)

            self._df = pd.concat([self._df, sheet_df], axis=1)

        self._df = self._df.T.drop_duplicates().T
        self._df.reset_index(inplace=True)

        self._df.rename(columns={"PERSONAL_DATA_AGE": "AGE", "PERSONAL_DATA_GENRE": "GENRE", "PERSONAL_DATA_EDUCATION": "EDUCATION", "PERSONAL_DATA_FREQUENCY_VR":"FREQUENCY_VR"}, inplace=True)

        #self._df.drop("index", axis=1, inplace=True)

        #print(self._df)
            #new_form_table = FormTable("form_{0}".format(name))
            #new_form_table._df = pd.read_excel("../data/{0}.xlsx".format(filename), sheet_name=name)
            #self._sheet_forms[name] = new_form_table
        
    # read_data_from_excel


    def analyse_data(self) -> None:
        super().analyse_data()

        self._results._df = self._df.copy()
        self._results._df.reset_index(inplace=True)
        self._results._df.drop(["index", "level_0", "ID"], axis=1, inplace=True)

        self.set_genres()
        
        #self._results._df = self._df.copy()
        #self._results._df.rename(columns={old_name: "[{0}_{1}]{2}".format(self._table_name, self._sheet_name, old_name) for old_name in self._results._df.columns})
    
    # analyse_data

    def set_user_id(self, user) -> None:
        pass
        #self._df.loc[self._df["user_id"] == user._user_name, "user_id"] = user._id
   

    #endregion
        
    #region METODOS PRIVADOS

    def rename_sheets_cols(self, df:pd.DataFrame, subfix:str) -> pd.DataFrame:
        df.rename(columns={old_name: "{0}_{1}".format(subfix.upper(), old_name.upper()) for old_name in df.columns}, inplace=True)
        df.rename(columns={"{0}_ID".format(subfix.upper()): "ID"}, inplace=True)

        return df
    
    def set_genres(self):
        self._results._df.loc[self._results._df["GENRE"] == "female", "GENRE"] = GenreType.F.name
        self._results._df.loc[self._results._df["GENRE"] == "male", "GENRE"] = GenreType.M.name
        self._results._df.loc[self._results._df["GENRE"] == "non_binary", "GENRE"] = GenreType.NB.name
        self._results._df.loc[self._results._df["GENRE"] == "other", "GENRE"] = GenreType.O.name

    #endregion
        


    