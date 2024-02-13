import pandas as pd

from structs.F_TablesList import TablesList

class GroupManager:
    '''
    Class GroupManager
    ------------------------------
    
    '''

    #region VARIABLES PUBLICAS

    _users: list

    _tables: TablesList

    _data: pd.DataFrame
    _results: pd.DataFrame

    #endregion


    #region METODOS PUBLICOS

    def __init__(self, users) -> None:
        self._users = users
        self._tables = TablesList()
        self._data = pd.DataFrame()
        self._results = pd.DataFrame()

    def set_data(self) -> None:
        for key in self._tables._data:
            self._tables._data[key].read_data_from_csv(key)

        # for user in self._users:
        #     self._tables._data["form_marks"].set_user_id(user)
            
        for key in self._tables._data:
            for user in self._users:
                if "user_id" in self._tables._data[key]._df.columns:
                    self._tables._data[key]._df.loc[self._tables._data[key]._df["user_id"] == user._id, "user_id"] = user._user_name
            self._tables._data[key].set_id_column()


    def analyse_data(self) -> None:
        for user in self._users:
            self._results = pd.concat([self._results, user.get_results()], axis=0)

    def export_results(self) -> None:
        self._results.to_csv("../results/global.csv")
        self._results.to_excel("../results/global.xlsx")

    def create_graphs(self) -> None:
        pass


    def get_table_data_by_user(self, table_name, user_name) -> pd.DataFrame:
        return self._tables._data[table_name].get_data_by_user(user_name)

    #endregion

    
    #region METODOS PRIVADOS

    #endregion