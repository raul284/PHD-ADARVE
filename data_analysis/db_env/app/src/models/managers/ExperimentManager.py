import pandas as pd
import os

from models.User import User


class ExperimentManager:
    '''
    Class Experiment
    -------------------

    La clase Experiment almacena toda la información referente a los experimentos. Contiene una lista de los usuarios
    que participan en el. 

    Extra resultados estadísticos, como medias o desviaciones, de cada uno de los escenarios y el total de todos ellos. 
    '''

#region VARIABLES GLOBALES

    _users: dict
    _results: pd.DataFrame

#endregion

#region METODOS

    
    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''
        # Recoge la información de los cuestionarios almacenados en CSVs
        self._users = {}
        self._results = pd.DataFrame()

    # __init__
        

    def set_data(self) -> None:
        self._users = self.get_users_dict()

        for id in self._users:
            self._users[id].set_data()

            if not os.path.exists("../data/{0}".format(id)):
                os.makedirs("../data/{0}".format(id))
            for table_name in self._users[id]._event_tables._data:
                file_path = "../data/{0}/{1}.csv".format(id, table_name)
                if not os.path.exists(file_path):
                    self._users[id]._event_tables.get_data_from_table(table_name).to_csv(file_path)
            for table_name in self._users[id]._form_tables._data:
                file_path = "../data/{0}/{1}.csv".format(id, table_name)
                if not os.path.exists(file_path):
                    self._users[id]._form_tables.get_data_from_table(table_name).to_csv(file_path)


        

    # set_data


    def analyse_data(self) -> None:
        '''Itera sobre los usuario para asignar sus resultados'''

        for id in self._users:
            self._users[id].analyse_data()

    # analyse_data

    
    def export_results(self) -> None:
        '''Exporta los resultados de los usuarios y posteriormente los datos globales del experimento'''

        if not os.path.exists("../results/csv"):
            os.makedirs("../results/csv")
        if not os.path.exists("../results/excel"):
            os.makedirs("../results/excel")

        for id in self._users:
            self._results = pd.concat([self._results, self._users[id].get_results()], axis=0).reset_index(drop=True)

        if not self._results.empty:
            all_results = self._results[self._results["SCENARIO"] == "ALL"]
            all_results.to_csv("../results/resultsALL.csv", na_rep='NULL')
            all_results.to_excel("../results/resultsALL.xlsx", na_rep='NULL')

            scenarios_results = self._results[self._results["SCENARIO"] != "ALL"]
            scenarios_results.to_csv("../results/resultsSCENARIO.csv", na_rep='NULL')
            scenarios_results.to_excel("../results/resultsSCENARIO.xlsx", na_rep='NULL')

    # export_results

    def get_users_dict(self) -> dict:
        users_dict = {}

        for dirpath, dirnames, filenames in os.walk("../data/"):
            for filename in [f for f in filenames if f == "users.csv"]:
                df = pd.read_csv(os.path.join(dirpath, filename))
                user_id = df.loc[0]["user_id"]

                if user_id not in users_dict:
                    users_dict[user_id] = User(
                        id = user_id,
                        experiment_id = df.loc[0]["experiment_id"],
                        group = df.loc[0]["user_group"],
                        hmd = df.loc[0]["hmd_type"],
                        event_datetime = df.loc[0]["event_datetime"])
        
        return users_dict

#endregion
