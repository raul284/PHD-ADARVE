import json, csv
import os

import database.db as db

from analysis.stress import *

from database.models import UserDB, GameplayEventDB, InteractEventDB, MoveEventDB

from objects.users.User import User
from objects.FieldStatistics import FieldStatistics


class Experiment:
    '''
    Class Experiment
    -------------------

    La clase Experiment almacena toda la información referente a los experimentos. Contiene una lista de los usuarios
    que participan en el. 

    Extra resultados estadísticos, como medias o desviaciones, de cada uno de los escenarios y el total de todos ellos. 
    '''

#region VARIABLES GLOBALES

    # Identificador del experimento
    id: int

    # Lista con los usuarios
    users: list

    # Datos del experimento. Dividido por cada uno de los escenarios y conjuntamente en unos datos globales.
    data: dict

    # Resultados del experimento. Dividido por cada uno de los escenarios y conjuntamente en unos datos globales.
    results: dict

#endregion

#region METODOS

    
    def __init__(self, id: int) -> None:
        '''Inicializa las propiedades de la clase.'''
        # Recoge la información de los cuestionarios almacenados en CSVs
        #form_manager = FormManager()
        #form_manager.form_to_dataframe()
        #calculate_stress()

        self.id = id
        if not os.path.exists("../results/exp{}".format(self.id)):
            os.makedirs("../results/exp{}".format(self.id))

        # Guarda la información de los usuarios que se encuentra en una base de datos MySQL
        db.Base.metadata.create_all(db.engine)

        self.users = []
        for user in db.session.query(UserDB).all():
            #if user.user_name != "All" and user.user_name != "Developer":
            if user.user_name in ["AACA", "AACD"]:
                if not os.path.exists("../results/exp{0}/{1}".format(self.id, user.user_name)):
                    os.makedirs("../results/exp{0}/{1}".format(self.id, user.user_name))
                self.users.append(User(db.session, user.user_name, self.id))

                
        # Inicialización del diccionario de datos
        self.data = {}
        self.data["global"] = {} # Datos globales
        self.data["scenarios"] = {} # Datos divididos en escenarios

        # Inicialización del diccionado de resultados
        self.results = {}
        self.results["global"] = {} # Resultados globales
        self.results["scenarios"] = {} # Resultados divididos en escenarios

    # __init__
        

    def set_users_data(self) -> None:
        '''Itera sobre los usuarios para asignar sus datos'''

        for user in self.users:
            user.set_data()

    # set_users_data

    def export_to_csv(self) -> None:
        '''Exporta todos los datos de la BD a CSVs'''

        with open("../results/exp{0}/gameplay.csv".format(self.id), "w", newline='') as outfile:
            writer = csv.writer(outfile)

            colnames = ["user_id", "scenary_type", "event_type", "event_datetime"]
            writer.writerow(colnames)

            for event in db.session.query(GameplayEventDB).all():
                if event.user_id != 1 and event.user_id != 2:
                    writer.writerow(event.as_dict().values())


        with open("../results/exp{0}/interact.csv".format(self.id), "w", newline='') as outfile:
            writer = csv.writer(outfile)

            colnames = ["user_id", "actor_id", "scenary_type", "event_type", "event_datetime"]
            writer.writerow(colnames)

            for event in db.session.query(InteractEventDB).all():
                if event.user_id != 1 and event.user_id != 2:
                    writer.writerow(event.as_dict().values())


        with open("../results/exp{0}/move.csv".format(self.id), "w", newline='') as outfile:
            writer = csv.writer(outfile)

            colnames = ["user_id", "scenary_type", "move_type", "start_datetime", "end_datetime", "start_position", "end_position", "distance"]
            writer.writerow(colnames)

            for event in db.session.query(MoveEventDB).all():
                if event.user_id != 1 and event.user_id != 2:
                    writer.writerow(event.as_dict().values())


        for user in self.users:
            user.export_to_csv()

    # export_to_csv

    def analyse_users(self) -> None:
        '''Itera sobre los usuario para asignar sus resultados'''
        
        for user in self.users:
            user.analyse_data()

    # analyse_users

    def set_global_data(self) -> None:
        '''Itera sobre los datos de los usuarios para obtener la informacion global
        del experimento'''

        # Recoge la informacion de los usuario para poder realizar el analisis global
        users_results = []
        #users_results = self.set_extra_users_to_global_data()
        #self.set_extra_users_to_global_data()
        for user in self.users:
            users_results.append(user.get_results_for_global_analysis())

        # Hace un merge entre los datos de los usuarios divididos por escenarios
        for result in users_results:
            self.merge_results(in_dict=result, out_dict=self.data["scenarios"], individual=True)
            
        # Hace un merge entre los usuarios para obtener unos datos globales
        for scenary in self.data["scenarios"]:
            self.merge_results(in_dict=self.data["scenarios"][scenary], out_dict=self.data["global"], individual=False)

    # set_global_data


    def analyse_global(self) -> None:
        '''Analiza los datos globales'''

        # Hace un analisis de datos para obtener unos resultados globales
        self.apply_statistics(in_dict=self.data["global"], out_dict=self.results["global"])

        # Hace un analisis de los datos de cada uno de los escenarios
        self.apply_statistics(in_dict=self.data["scenarios"], out_dict=self.results["scenarios"])

    # analyse_global

    
    def export_results(self) -> None:
        '''Exporta los resultados de los usuarios y posteriormente los datos globales del experimento'''

        for user in self.users:
            user.export_results()

        with open("../results/exp{0}/experiment_results.json".format(self.id), "w") as outfile:
            json.dump(self.results, outfile, indent=4)

    # export_results


    def merge_results(self, in_dict: dict, out_dict: dict, individual: bool) -> None:
        '''
        Metodo que se lanza recursivamente. Accede a cada una de las variables de los diccionarios y 
        las introduce en otro en forma de lista.
        
        :param in_dict: Diccionario con los datos de entrada
        :param out_dict: Diccionario con los datos de salida
        :param individual: Booleano que controla si se tratan los datos como escenarios individuales o como experimento global.
        '''

        # En el caso de que el dato de entrada no sea diccionario, se devuelve este mismo dato
        if type(in_dict) is not dict:
            return in_dict

        # Por cada clave-valor del diccionario de entrada
        for key, value in in_dict.items():
            
            # Si el valor es un diccionario
            if type(value) == dict:

                # Si la clave no se encuentra aun en el diccionario de salida, crea un diccionario vacio
                if key not in out_dict:
                    out_dict[key] = {}

                # Hace recursion sobre este valor (diccionario)
                self.merge_results(value, out_dict[key], individual)

            # Si no es un diccionario
            else:
                
                # Si la clave no se encuentra en el diccionario de salida, se crea una lista vacia
                if key not in out_dict:
                    out_dict[key] = []

                # En el caso de que sean por escenarios individuales se encontraran valores de tipos simples como int o str
                # y se añadirian a la lista creada
                if individual: 
                    out_dict[key].append(value) 
                # En el caso de que seaglobal se encontraran valores de tipos complejos como listas. Se añadirian a la lista creada.
                else:
                    out_dict[key] = out_dict[key] + value

    # merge_results


    def apply_statistics(self, in_dict: dict, out_dict: dict) -> None:
        '''
        Accede recursivamente a cada uno de los datos del experimento y le aplica la estadistica.
        
        :param in_dict: Diccionario de entrada
        :param out_dict: Diccionario de salida
        '''

        # Si el valor de entrada no es un diccionario, devuelve ese mismo valor
        if type(in_dict) is not dict:
            return in_dict

        # Por cada clave-valor del diccionario de entrada
        for key, value in in_dict.items():
            
            # Si el valor es un diccionario
            if type(value) == dict:
                
                # Si la clave no se encuentra aun en el diccionario de salida, crea un diccionario vacio
                if key not in out_dict:
                    out_dict[key] = {}

                # Hace recursion sobre este valor (diccionario)
                self.apply_statistics(value, out_dict[key])

            # Si el valor es una lista (lo mas normal es que sea una lista ya que anteriormente hemos hecho un 
            # merge para que fueran listas de datos)
            elif type(value) == list:
                
                # Se crea el campo de la estadistica
                field_stats = FieldStatistics()
                # Se aplican valores
                field_stats.add_values(value)
                # Se guardan los resultados en el nuevo campo
                out_dict[key] = field_stats.get_statistics()

    # apply_statistics

#endregion
