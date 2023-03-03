import json

from database.models import UserDB
from objects.scenarios.CarAccidentScenary import CarAccidentScenary
from objects.scenarios.LaboratoryScenary import LaboratoryScenary


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
    ids: list

    # Datos del usuario
    data: dict

    # Resultados del usuario
    results: dict

#endregion

#region METODOS

    def __init__(self, db, name: str) -> None:
        '''
        Inicializa las propiedades de la clase.
        
        :param db: Referencia  al base de datos
        :param name: Nombre del usuario
        '''

        self.db = db
        self.name = name

        # Busca los identificadores que esten relacionados con el nombre de usuario en la base de datos.
        self.ids = self.db.query(UserDB).filter(UserDB.user_name == name).all()

        self.data = {}
        self.results = {}

    # __init__


    def set_data(self) -> None:
        '''Asigna la informacion relacionada con el usuario. Esta informacion esta dividida en escenarios (Scenary)
        que forman la experiencia'''

        self.data = {
            "car_accident": CarAccidentScenary(db=self.db, user_ids=[ self.ids[0].id,  self.ids[1].id]),
            "laboratory": LaboratoryScenary(db=self.db, user_ids=[ self.ids[0].id,  self.ids[1].id])
        }

        # Itera sobre cada uno de los escenarios para que asignen sus datos
        for key in self.data:
            self.data[key].set_data()

    # set_data

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

        with open("../results/users/{}.json".format(self.name), "w") as outfile:
            json.dump(self.results, outfile, indent=4)

    # export_results

#endregion

        

    