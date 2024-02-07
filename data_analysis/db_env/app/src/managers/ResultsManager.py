import pandas as pd

class ResultsManager:
    '''
    Class ResultsManager
    ----------------------------
    '''

    #region VARIABLES PUBLICAS

    _users: list

    _tables_results: dict

    _global_results: pd.DataFrame

    #endregion


    #region METODOS PUBLICOS

    def __init__(self) -> None:
        self._users = []
        self._tables_results = {}
        self._global_results = pd.DataFrame()

    def set_data(self, users) -> None:
        self._users = users
        self.set_tables_results(self._users)
        self.set_global_results()

    def export_results(self) -> None:
        for table in self._tables_results:
            self._tables_results[table].to_csv("../results/tables/{0}.csv".format(table))

        users_with_ingame_tips = [user._id for user in self._users if user._tips_ingame_enabled]

        self._global_results[self._global_results["user_id"].isin(users_with_ingame_tips)].to_csv("../results/ingame_tips.csv")
        self._global_results[~self._global_results["user_id"].isin(users_with_ingame_tips)].to_csv("../results/paper_tips.csv")

        self._global_results.to_csv("../results/global.csv")

    #endregion


    #region METODOS PRIVADOS

    def set_tables_results(self, users):
        for user in users:
            aux_result_tables = user.get_results()
            for key in aux_result_tables:
                aux_df = pd.concat([pd.DataFrame({"user_id": [int(user._id)]}), aux_result_tables[key]], axis=1)

                if key not in self._tables_results:
                    self._tables_results[key] = pd.DataFrame()
                
                self._tables_results[key] = pd.concat([self._tables_results[key], aux_df], axis=0)

    def set_global_results(self):
        
        for tables in self._tables_results:
            if self._global_results.empty:
                self._global_results = pd.concat([self._global_results, self._tables_results[tables]])
            else:
                self._global_results = self._global_results.merge(self._tables_results[tables], on = 'user_id', how = 'left')


    #endregion