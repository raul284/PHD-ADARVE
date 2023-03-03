from database.models import InteractEventDB, GameplayEventDB, MoveEventDB
from objects.phases.Phase import Phase

class Scenary:

    '''
    Class Scenary
    -------------------

    Contiene la informacion relativa a los escenarios. Esta informacion esta relacionada solo con un
    unico usuarios ya que la relación es inversa, es decir, un usuario tiene varios escenarios. 

    Los datos y resultados se dividen en dos partes. (1) "tutorial" se refiere a la prueba guiada
    y (2) "game" se relaciona con la parte libre donde el usuario tendra que poner en practica lo aprendido.
    '''

#region VARIABLES GLOBALES

    # Acceso a la base de datos
    db: None

    # Ids del usuario. La lista siempre debe estar formada por 2 valores, uno para el tutorial y otro para el juego.
    user_ids: list

    # Diccionario con los datos del escenario
    data: dict

    # Diccionario con los resultados del escenario
    results: dict

#endregion

#region METODOS

    def __init__(self, db, user_ids: list):
        '''Inicializa las propiedades de la clase.'''

        self.db = db
        self.user_ids = user_ids

        self.data = {}
        self.results = {}
    
    # __init__
        

    def set_data(self) -> None:
        '''
        Asigna la informacion relacionada con cada una de las partes del escenario (Phase). Cada una de ellas
        es una fase formada por listas de tipos de eventos. 
        '''

        self.data = {
            "tutorial": self.set_phase(self.user_ids[0]),
            "game": self.set_phase(self.user_ids[1])
        }

    # set_data


    def set_phase(self, id: int) -> Phase:
        '''
        Crea un objeto de tipo Phase, y lo devuelve, con los datos las interacciones que ha realizado el usuario con el
        identificador indicado.

        :param id: Identificado del usuario en la base de datos
        :return: Devuelve un objeto de tipo Phase
        '''

        # Crea el objeto de tipo clase
        phase = Phase()

        # Asigna los datos de la fase. Para ello coge la informacion de la base de datos en base al indentificador.
        # La informacion se divide en N listas siendo N el numero de tipos de interacciones distintas. La lista que
        # proporciona la base de datos se ordena segun el instante de tiempo que se realizo dicho evento.
        #
        phase.set_data(
            # Lista de los objetivos del gameplay
            sorted(
                [event.as_dict() for event in self.db.query(GameplayEventDB).filter(GameplayEventDB.user_id == id).all()], 
                key=lambda d: d["event_datetime"]),
            # Lista de las interacciones realizadas con los objetos
            sorted(
                [event.as_dict() for event in self.db.query(InteractEventDB).filter(InteractEventDB.user_id == id).all()], 
                key=lambda d: d["event_datetime"]),
            # Lista de los movimientos que realizan los usuarios
            sorted(
                [event.as_dict() for event in self.db.query(MoveEventDB).filter(MoveEventDB.user_id == id).all()],
                key=lambda d: d["start_datetime"])
        )

        # Devuelve la fase
        return phase

    # set_phases


    def get_data(self) -> dict:
        '''
        Devuelve los datos del escenario
        
        :return: Datos del escenario
        '''

        return self.data

    # get_data


    def analyse_data(self) -> None:
        '''Analiza los datos de cada una de las fases y las almacena en los resultados del escenario'''

        # Itera sobre los escenarios y analiza sus datos
        for key in self.data:
            self.data[key].analyse_data()
            self.results[key] = self.data[key].get_results()

    # analyse_data
            
    def get_results(self) -> dict:
        '''
        Devuelve los resultados del escenario
        
        :return: Resultados del escenario
        '''

        return self.results

    # get_results


    def get_results_for_global_analysis(self) -> dict:
        '''
        Hace un filtrado de los resultados del escenario son los necesarios para realizar el analisis.
        Por ejemplo, la lista de interacciones realizadas no es necesaria, pero el numero de interacciones
        realizadas si.

        :return: Resultados del escenario para hacer el analisis
        '''

        return {
            key: self.data[key].get_results_for_global_analysis() for key in self.data
        }

    # get_results_for_global_analysis

#endregion

        