import json, csv
import pandas as pd

from database.models import UserDB
from objects.scenarios.SandboxScenario import SandboxScenario
from objects.scenarios.TutorialScenario import TutorialScenario
from objects.scenarios.CarAccidentScenario import CarAccidentScenario


class User:
    '''
    Class User
    -------------------

    ...
    '''

#region VARIABLES GLOBALES

    # Acceso a la base de datos
    db: None

    # Nombre del usuario. Este nombre sirve para buscar los identificadores en la base
    # de datos y relacionarlos con los cuestionarios online.
    name: str

    # Lista de identificadores de los usuarios. Cada usuario debe tener N*2 siendo N
    # el numero de escenarios.
    id: int

    # Datos del usuario
    data: dict

    # Resultados del usuario
    results: dict

    # Identificador del experimento
    experiment_id: int

#endregion

#region METODOS

    def __init__(self, db, name: str, experiment_id: int) -> None:
        '''
        Inicializa las propiedades de la clase.
        
        :param db: Referencia  al base de datos
        :param name: Nombre del usuario
        '''

        self.db = db
        self.name = name

        # Busca los identificadores que esten relacionados con el nombre de usuario en la base de datos.
        self.id = self.db.query(UserDB).filter(UserDB.user_name == name).all()[0].id

        self.data = {}
        self.results = {}

        self.experiment_id = experiment_id

    # __init__


    def set_data(self) -> None:
        '''Asigna la informacion relacionada con el usuario. Esta informacion esta dividida en escenarios (Scenary)
        que forman la experiencia'''

        self.data = {
            "sandbox": SandboxScenario(user_id=self.id, experiment_id=self.experiment_id),
            "tutorial": TutorialScenario(user_id=self.id, experiment_id=self.experiment_id),
            "car_accident": CarAccidentScenario(user_id=self.id, experiment_id=self.experiment_id),
        }

        # Itera sobre cada uno de los escenarios para que asignen sus datos
        for key in self.data:
            self.data[key].set_data()

    # set_data

    def export_to_csv(self) -> None:
        '''Exporta todos los datos de la BD a CSVs'''

        aux_dataframes_gameplay = []
        aux_dataframes_interact = []
        aux_dataframes_move = []

        for scenary in self.data:
            if "gameplay" in self.data[scenary].data:
                aux_dataframes_gameplay.append(self.data[scenary].data["gameplay"].events)
            if "interact" in self.data[scenary].data:
                aux_dataframes_interact.append(self.data[scenary].data["interact"].events)
            if "move" in self.data[scenary].data:
                aux_dataframes_move.append(self.data[scenary].data["move"].events)

        pd.concat(aux_dataframes_gameplay).to_csv("../results/exp{0}/{1}/gameplay.csv".format(self.experiment_id, self.name), index=False)     
        pd.concat(aux_dataframes_interact).to_csv("../results/exp{0}/{1}/interact.csv".format(self.experiment_id, self.name), index=False)     
        pd.concat(aux_dataframes_move).to_csv("../results/exp{0}/{1}/move.csv".format(self.experiment_id, self.name), index=False)     

        '''with open("../results/exp{0}/{1}/gameplay.csv".format(self.experiment_id, self.name), "w", newline='') as outfile:
            writer = csv.writer(outfile)

            colnames = ["user_id", "scenary_type", "event_type", "event_datetime"]
            writer.writerow(colnames)

            aux_dataframes = []
            for scenary in self.data:
                if "gameplay" in self.data[scenary].data:
                    print(self.data[scenary].data["gameplay"])
                    aux_dataframes.append(self.data[scenary].data["gameplay"])
                    for event in self.data[scenary].data["gameplay"].events:
                        writer.writerow(event.values())


        with open("../results/exp{0}/{1}/interact.csv".format(self.experiment_id, self.name), "w", newline='') as outfile:
            writer = csv.writer(outfile)

            colnames = ["user_id", "actor_id", "scenary_type", "event_type", "event_datetime"]
            writer.writerow(colnames)

            for scenary in self.data:
                if "interact" in self.data[scenary].data:
                    for event in self.data[scenary].data["interact"].events:
                        writer.writerow(event.values())


        with open("../results/exp{0}/{1}/move.csv".format(self.experiment_id, self.name), "w", newline='') as outfile:
            writer = csv.writer(outfile)

            colnames = ["user_id", "scenary_type", "move_type", "start_datetime", "end_datetime", "start_position", "end_position", "distance"]
            writer.writerow(colnames)

            for scenary in self.data:
                if "move" in self.data[scenary].data:
                    for event in self.data[scenary].data["move"].events:
                        writer.writerow(event.values())
        '''


    # export_to_csv

    def get_data(self) -> dict:
        '''
        Devuelve los datos del usuario
        
        :return: Datos del usuario
        '''

        return self.data

    # get_data

    def analyse_data(self) -> None:
        '''Analiza los datos de cada una de los escenarios y las almacena en los resultados del usuario'''

        for key in self.data:
            self.data[key].analyse_data()
            self.results[key] = self.data[key].get_results()

    # analyse_data

    def get_results(self) -> dict:
        '''
        Devuelve los resultados del usuario
        
        :return: Resultados del usuario
        '''

        return self.results

    # get_results

    def get_results_for_global_analysis(self) -> dict:
        '''
        Hace un filtrado de los resultados del usuario para poder hacer el analisis global.
        Estos datos vienen por parte de los escenarios.
        
        :return: Resultados filtrados
        '''

        return {
            key: self.data[key].get_results_for_global_analysis() for key in self.data
        }

    # get_results_for_global_analysis

    def export_results(self) -> None:
        '''Exporta los resultados del usuario en un archivo de tipo JSON con el nombre del usuario'''

        with open("../results/exp{0}/{1}/{1}.json".format(self.experiment_id, self.name), "w") as outfile:
            print(self.results)
            json.dump(self.results, outfile, indent=4)

    # export_results

#endregion

        

    