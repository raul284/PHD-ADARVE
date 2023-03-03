from objects.events.GameplayEvents import GameplayEvents
from objects.events.InteractEvents import InteractEvents
from objects.events.MoveEvents import MoveEvents

class Phase:
    '''
    Class Phase
    -------------------
    
    ...
    '''

#region VARIABLES GLOBALES

    # ...
    data: dict

    # ...
    results: dict

    # ...
    start_time: str

    # ...
    end_time: str

    # ...
    duration: str

    # ...
    gameplay_events: GameplayEvents

    # ...
    interact_events: InteractEvents

    # ...
    move_events: MoveEvents

#endregion

#region METODOS

    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''

        self.data = {}
        self.results = {}
        #self.transform_dates()

    # __init__

    def set_data(self, gameplay_events, interact_events, move_events) -> None:
        '''
        Asigna la informacion relacionada con cada una de los tipos de interacciones (Events). 

        :param gameplay_events: Lista de eventos lanzados por los objetivos del gameplay
        :param interact_events: Lista de eventos lanzados por las interacciones con los objetos
        :param move_events: Lista de eventos relacionados con el movimiento del usuario
        '''

        self.data = {
            "gameplay": GameplayEvents(gameplay_events),
            "interact": InteractEvents(interact_events),
            "move": MoveEvents(move_events)
        }

        # Informacion relacionada con el tiempo de la fase
        self.set_time_info()

    # set_data

    def get_data(self) -> dict:
        '''
        Devuelve los datos de la fase
        
        :return: Datos de la fase
        '''

        return self.data

    #get_data

    def set_time_info(self) -> None:
        '''Asigna la informacion relacionada con el tiempo. Tiempo de inicio, tiempo de fin y duracion.'''

        # Busca el evento de "Start" que indique el inicio de la fase
        start_time_in_seconds = self.data["gameplay"].get_event_of_type("Start")["event_datetime"]
        # Busca el evento de "Finish que indique el fin de la fase"
        end_time_in_seconds = self.data["gameplay"].get_event_of_type("Finish")["event_datetime"]

        #self.start_time = datetime.fromtimestamp(start_time_in_seconds).strftime("%Y-%m-%d %H:%M:%S")
        #self.end_time = datetime.fromtimestamp(end_time_in_seconds).strftime("%Y-%m-%d %H:%M:%S")
        #self.duration = datetime.fromtimestamp(end_time_in_seconds - start_time_in_seconds).strftime("%M:%S")
        self.start_time = start_time_in_seconds
        self.end_time = end_time_in_seconds
        self.duration = end_time_in_seconds - start_time_in_seconds

    # set_time_info

    def analyse_data(self) -> None:
        '''Analiza los datos de la fase.'''

        self.results = {
            "time_info": {
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.duration
                }, 
            "events": {
                key : self.data[key].get_results() for key in self.data
                }
        }

    # analyse_data

    def get_results(self) -> dict:
        '''
        Devuelve los resultados de la fase
        
        :return: Resultados de la fase
        '''

        return self.results

    # get_results

    def get_results_for_global_analysis(self) -> dict:
        '''
        Hace un filtrado de los resultados de la fase para poder hacer el analisis global.
        
        :return: Resultados filtrados
        '''

        return {
            "time_info": {
                "duration": self.duration
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

#endregion
        