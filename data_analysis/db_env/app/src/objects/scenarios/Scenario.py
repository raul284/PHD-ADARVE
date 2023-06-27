from database.models import InteractEventDB, GameplayEventDB, MoveEventDB
from objects.events.GameplayEvents import GameplayEvents
from objects.events.InteractEvents import InteractEvents
from objects.events.MoveEvents import MoveEvents

import pandas as pd

class Scenario:

    '''
    Class Scenario
    -------------------

    Contiene la informacion relativa a los escenarios. Esta informacion esta relacionada solo con un
    unico usuarios ya que la relación es inversa, es decir, un usuario tiene varios escenarios. 

    Los datos y resultados se dividen en dos partes. (1) "tutorial" se refiere a la prueba guiada
    y (2) "game" se relaciona con la parte libre donde el usuario tendra que poner en practica lo aprendido.
    '''

#region VARIABLES GLOBALES

    # Nombre que recibe el escenario en la base de datos
    scenario_type: str

    # Booleano de control que indica si el usuario ha entrado en el escenario. En el caso de que no, entonces no se hace nada
    user_enter_into_scenario: bool

    # Ids del usuario. La lista siempre debe estar formada por 2 valores, uno para el tutorial y otro para el juego.
    user_id: int

    # Identificador del experimento
    experiment_id: int

    # Diccionario con los datos del escenario
    data: dict

    # Diccionario con los resultados del escenario
    results: dict

    # ...
    start_time: str

    # ...
    end_time: str

    # ...
    duration: str


#endregion

#region METODOS

    def __init__(self, user_id: int, experiment_id: int):
        '''Inicializa las propiedades de la clase.'''

        self.user_id = user_id
        self.experiment_id = experiment_id

        self.data = {}
        self.results = {}
    
    # __init__
        

    def set_data(self) -> None:
        '''
        Asigna la informacion relacionada con cada una de las partes del escenario (Phase). Cada una de ellas
        es una fase formada por listas de tipos de eventos. 
        '''

        df_gameplay = pd.read_csv("../results/exp{0}/gameplay.csv".format(self.experiment_id))
        df_interact = pd.read_csv("../results/exp{0}/interact.csv".format(self.experiment_id))
        df_move = pd.read_csv("../results/exp{0}/move.csv".format(self.experiment_id))

        '''db_gameplay_events = self.db.query(GameplayEventDB).\
             filter(GameplayEventDB.scenary_type == self.scenario_type).\
                filter(GameplayEventDB.user_id == self.user_id).all()
        
        gameplay_events = sorted(
            [event.as_dict() for event in db_gameplay_events], 
            key=lambda d: d["event_datetime"])
        
        db_interact_events = self.db.query(InteractEventDB).\
             filter(InteractEventDB.scenary_type == self.scenario_type).\
                filter(InteractEventDB.user_id == self.user_id).all()
        interact_events = sorted(
            [event.as_dict() for event in db_interact_events], 
            key=lambda d: d["event_datetime"])
        
        
        db_move_events = self.db.query(MoveEventDB).\
             filter(MoveEventDB.scenary_type == self.scenario_type).\
                filter(MoveEventDB.user_id == self.user_id).all()
        move_events = sorted(
            [event.as_dict() for event in db_move_events],
            key=lambda d: d["start_datetime"])'''


        self.data = {
            "gameplay": GameplayEvents(
                df_gameplay.loc[
                    (df_gameplay['user_id'] == self.user_id) & 
                    (df_gameplay['scenary_type'] == self.scenario_type)
                    ].sort_values(by=["event_datetime"])),
            "interact": InteractEvents(
                df_interact.loc[
                    (df_interact['user_id'] == self.user_id) & 
                    (df_interact['scenary_type'] == self.scenario_type)
                    ].sort_values(by=["event_datetime"])),
            "move": MoveEvents(
                df_move.loc[
                    (df_move['user_id'] == self.user_id) & 
                    (df_move['scenary_type'] == self.scenario_type)
                    ].sort_values(by=["start_datetime"]))
        }

        if len(self.data["gameplay"].events) > 0:
            self.set_time_info()

        '''self.user_enter_into_scenario = gameplay_events and interact_events and move_events
        
        if self.user_enter_into_scenario:
            self.data = {
                "gameplay": GameplayEvents(gameplay_events),
                "interact": InteractEvents(interact_events),
                "move": MoveEvents(move_events)
            }

                # Informacion relacionada con el tiempo de la fase
            if "gameplay" in self.data:
                self.set_time_info()'''

    # set_data


    def get_data(self) -> dict:
        '''
        Devuelve los datos del escenario
        
        :return: Datos del escenario
        '''

        return self.data

    # get_data

    def set_time_info(self) -> None:
        '''Asigna la informacion relacionada con el tiempo. Tiempo de inicio, tiempo de fin y duracion.'''

        # Busca el evento de "Start" que indique el inicio de la fase
        start_time_in_seconds = self.data["gameplay"].get_first_event_of_type("Start")["event_datetime"]
        # Busca el evento de "Finish que indique el fin de la fase"
        end_time_in_seconds = self.data["gameplay"].get_last_event_of_type("Finish")["event_datetime"]

        #self.start_time = datetime.fromtimestamp(start_time_in_seconds).strftime("%Y-%m-%d %H:%M:%S")
        #self.end_time = datetime.fromtimestamp(end_time_in_seconds).strftime("%Y-%m-%d %H:%M:%S")
        #self.duration = datetime.fromtimestamp(end_time_in_seconds - start_time_in_seconds).strftime("%M:%S")
        self.start_time = start_time_in_seconds
        self.end_time = end_time_in_seconds
        self.duration = end_time_in_seconds - start_time_in_seconds


    def analyse_data(self) -> None:
        '''Analiza los datos de cada una de las fases y las almacena en los resultados del escenario'''

        # Itera sobre los escenarios y analiza sus datos
        """ for key in self.data:
            self.data[key].analyse_data()
            self.results[key] = self.data[key].get_results() """

        if not self.scenary_without_data():
            for key in self.data:
                self.data[key].analyse_data()
        
            self.results = {
                "time_info": {
                    "start_time": int(self.start_time),
                    "end_time": int(self.end_time),
                    "duration": int(self.duration)
                    }, 
                "events": {
                    key : self.data[key].get_results() for key in self.data
                    }
            }

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
        '''if self.user_enter_into_scenario:
            return {
                "time_info": {
                    "duration": self.duration
                },
                "events": {
                    key : self.data[key].get_results_for_global_analysis() for key in self.data
                }
            }
        return {}'''

        if self.scenary_without_data():
            return {}
        else:
            return {
                    "time_info": {
                        "duration": int(self.duration)
                    },
                    "events": {
                        key : self.data[key].get_results_for_global_analysis() for key in self.data
                    }
                }

    # get_results_for_global_analysis

    def transform_dates(self) -> None:
        '''Transforma el formato de las fechas. En un principio estos valores estan en numero de segundos
        y se quiere transformar a una fecha con formato de DD/MM/AA - HH:MM:SS'''

        #self.gameplay_events.transform_dates()
        #self.interact_events.transform_dates()
        #self.move_events.transform_dates()

        pass

    # transform_dates

    def scenary_without_data(self) -> bool:
        return len(self.data["gameplay"].events) == 0

#endregion

        