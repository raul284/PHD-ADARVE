import pandas as pd
import os

from models.User import User
from models.Group import Group
from models.form.Form import Form

from models.events import *
from models.tables import *


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

    _form: Form

#endregion

#region METODOS

    
    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''
        # Recoge la información de los cuestionarios almacenados en CSVs
        #form_manager = FormManager()
        #form_manager.form_to_dataframe()
        self._users = {}
        self._form = Form()

    # __init__
        

    def set_data(self) -> None:
        self._users = self.get_users_dict()

        for id in self._users:
            self._users[id].set_data()

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

        results = {}

        for id in self._users:
            user_results = self._users[id].get_results()
            for table in user_results:
                if table not in results:
                    results[table] = pd.DataFrame()

                #print(table, user_results[table])
                results[table] = pd.concat([results[table], user_results[table]], ignore_index=True)
        
        for table in results:
            results[table].to_csv("../results/csv/{0}.csv".format(table))
            results[table].to_excel("../results/excel/{0}.xlsx".format(table))

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
                        group = df.loc[0]["user_group"],
                        hmd = df.loc[0]["hmd_type"],
                        event_datetime = df.loc[0]["event_datetime"])
        
        
        return users_dict

#endregion
