import json

import database.db as db

from analysis.stress import *

from form.FormManager import FormManager


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

    # Lista con los usuarios
    users: list

    # Datos del experimento. Dividido por cada uno de los escenarios y conjuntamente en unos datos globales.
    data: dict

    # Resultados del experimento. Dividido por cada uno de los escenarios y conjuntamente en unos datos globales.
    results: dict

#endregion

#region METODOS

    
    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''
        # Recoge la información de los cuestionarios almacenados en CSVs
        #form_manager = FormManager()
        #form_manager.form_to_dataframe()
        #calculate_stress()

        # Guarda la información de los usuarios que se encuentra en una base de datos MySQL
        db.Base.metadata.create_all(db.engine)

        self.users = []
        for name in ["AABA", "AABB"]:
            self.users.append(User(db.session, name))

        #self.users = [User(db.session, "Ale"), User(db.session, "Ale")] # TEMPORAL
        #for id in form_manager.main_info_form._df["id"]:
            #users_db = db.session.query(UserDB).filter(UserDB.user_name == id).all()
            #self.users.append(User(db.session, id))

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


    def analyse_users(self) -> None:
        '''Itera sobre los usuario para asignar sus resultados'''
        
        for user in self.users:
            user.analyse_data()

    # analyse_users
    
    def set_extra_users_to_global_data(self) -> None:
        results = []
        for name in ["AAAA", "AAAB", "AAAC"]:
            f = open('../results/users/{0}.json'.format("AAAA"))
            data = json.load(f)

            aux_dict = {
                "car_accident": {
                    "tutorial": {
                        "time_info": {
                            "duration": data["phase"]["guided"]["duration"]
                        },
                        "events": {
                            "gameplay": {
                                "numOfInteractions":{
                                    "with_rep": data["events"]["gameplay"]["guided"]["numOfInteractions"]["with_rep"],
                                    "without_rep": data["events"]["gameplay"]["guided"]["numOfInteractions"]["without_rep"],
                                },
                                "meanTimeBetweenInteraction": {
                                    "with_rep": data["events"]["gameplay"]["guided"]["meanTimeBetweenInteraction"]["with_rep"],
                                    "without_rep": data["events"]["gameplay"]["guided"]["meanTimeBetweenInteraction"]["without_rep"],
                                }
                            },
                            "interact":{
                                "numOfInteractions":{
                                    "with_rep": data["events"]["interact"]["guided"]["numOfInteractions"]["with_rep"],
                                    "without_rep": data["events"]["interact"]["guided"]["numOfInteractions"]["without_rep"],
                                },
                                "meanTimeBetweenInteraction": {
                                    "with_rep": data["events"]["interact"]["guided"]["meanTimeBetweenInteraction"]["with_rep"],
                                    "without_rep": data["events"]["interact"]["guided"]["meanTimeBetweenInteraction"]["without_rep"],
                                }
                            }
                        }
                    },
                    "game":{
                        "time_info": {
                            "duration": data["phase"]["nonguided"]["duration"]
                        },
                        "events": {
                            "gameplay": {
                                "numOfInteractions":{
                                    "with_rep": data["events"]["gameplay"]["nonguided"]["numOfInteractions"]["with_rep"],
                                    "without_rep": data["events"]["gameplay"]["nonguided"]["numOfInteractions"]["without_rep"],
                                },
                                "meanTimeBetweenInteraction": {
                                    "with_rep": data["events"]["gameplay"]["nonguided"]["meanTimeBetweenInteraction"]["with_rep"],
                                    "without_rep": data["events"]["gameplay"]["nonguided"]["meanTimeBetweenInteraction"]["without_rep"],
                                }
                            },
                            "interact":{
                                "numOfInteractions":{
                                    "with_rep": data["events"]["interact"]["nonguided"]["numOfInteractions"]["with_rep"],
                                    "without_rep": data["events"]["interact"]["nonguided"]["numOfInteractions"]["without_rep"],
                                },
                                "meanTimeBetweenInteraction": {
                                    "with_rep": data["events"]["interact"]["nonguided"]["meanTimeBetweenInteraction"]["with_rep"],
                                    "without_rep": data["events"]["interact"]["nonguided"]["meanTimeBetweenInteraction"]["without_rep"],
                                }
                            }
                        }
                    }
                }
            }

            results.append(aux_dict)
        return results

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

        with open("../results/{}.json".format("experiment_results"), "w") as outfile:
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
