import pandas as pd

from models.User import User

from models.events import *
from models.tables import *

from managers.DataManager import DataManager
from managers.ResultsManager import ResultsManager


class Experiment:
    '''
    Class Experiment
    -------------------

    La clase Experiment almacena toda la información referente a los experimentos. Contiene una lista de los usuarios
    que participan en el. 

    Extra resultados estadísticos, como medias o desviaciones, de cada uno de los escenarios y el total de todos ellos. 
    '''

#region VARIABLES GLOBALES

    # Lista con los usuarios
    _users: list
    _user_type_ids: dict

    # Datos del experimento. Dividido por cada uno de los escenarios y conjuntamente en unos datos globales.
    _data_manager: DataManager

    _results_manager: ResultsManager

#endregion

#region METODOS

    
    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''
        # Recoge la información de los cuestionarios almacenados en CSVs
        #form_manager = FormManager()
        #form_manager.form_to_dataframe()
        self._users = []
        self._data_manager = DataManager(True)
        self._results_manager = ResultsManager()

    # __init__
        
    def set_data(self) -> None:

        users_df = pd.read_csv("../data/users.csv")
        self._users = [User(*users_df.iloc[index].to_list()) for index in users_df.index]

        self._data_manager.set_data()

        for key in self._data_manager._tables:
            self._data_manager._tables[key].read_data_from_csv(key)

        for user in self._users:
            user.set_data()
            for key in self._data_manager._tables:
                user._data_manager._tables[key]._df = self._data_manager._tables[key].get_data_dataframe_by_user(user._id)
                user._data_manager._tables[key]._list = self._data_manager._tables[key].get_data_list_by_user(user._id)
    
    # set_data

    def analyse_data(self) -> None:
        '''Itera sobre los usuario para asignar sus resultados'''
        
        #self._data_manager.analyse_data()

        for user in self._users:
            user.analyse_data()
            #print(user._data_manager._tables["item_interaction_events"]._results._df)

        self._results_manager.set_data(self._users)

        #print(self._data_manager.get_joined_results())

    # analyse_data

    
    def export_results(self) -> None:
        '''Exporta los resultados de los usuarios y posteriormente los datos globales del experimento'''

        self._results_manager.export_results()

    # export_results

    def create_graphs(self) -> None:
        for user in self._users:
            user.create_graphs()

#endregion
