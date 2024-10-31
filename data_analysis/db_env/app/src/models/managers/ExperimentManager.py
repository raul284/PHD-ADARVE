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

#endregion

#region METODOS

    
    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''
        # Recoge la información de los cuestionarios almacenados en CSVs
        self._users = {}

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

        results = {
            "events":{},
            "form":{}
        }

        for id in self._users:
            event_results = self._users[id].get_event_results()
            for table in event_results:
                if table not in results["events"]:
                    results["events"][table] = pd.DataFrame()
                results["events"][table] = pd.concat([results["events"][table], event_results[table]], axis=0, ignore_index=True)

            form_results = self._users[id].get_form_results()
            for table in form_results:
                if table not in results["form"]:
                    results["form"][table] = pd.DataFrame()
                results["form"][table] = pd.concat([results["form"][table], form_results[table]], ignore_index=True)          

        experiment_results = pd.DataFrame()
        for table in results["events"]:
            if len(experiment_results) > 0:
                results["events"][table] = results["events"][table].drop(columns=['ID', 'GROUP', 'HMD', 'SCENARIO'], axis=1, errors='ignore')
            experiment_results = pd.concat([experiment_results, results["events"][table]], axis=1)
        
        for table in results["form"]:
            aux_df = pd.DataFrame()
            for index, row in results["form"][table].iterrows():
                for i in range(int(len(experiment_results) / len(self._users))):
                    aux_df = pd.concat([aux_df, results["form"][table].iloc[index]], axis=1, ignore_index=True) 
            experiment_results = pd.concat([experiment_results, aux_df.T], axis=1)

        #print(experiment_results)

        if len(experiment_results) > 0:
            experiment_results[experiment_results["SCENARIO"] == "ALL"].to_csv("../results/resultsALL.csv", na_rep='NULL')
            experiment_results[experiment_results["SCENARIO"] == "ALL"].to_excel("../results/resultsALL.xlsx", na_rep='NULL')

            experiment_results[experiment_results["SCENARIO"] != "ALL"].to_csv("../results/resultsSCENARIO.csv", na_rep='NULL')
            experiment_results[experiment_results["SCENARIO"] != "ALL"].to_excel("../results/resultsSCENARIO.xlsx", na_rep='NULL')

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
