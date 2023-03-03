import statistics
from datetime import datetime

from objects.events.Events import Events

class MoveEvents(Events):

    # Distancia total recorrida
    total_distance: float

    def __init__(self, raw_data) -> None:
        super().__init__(raw_data)
        
        self.set_total_distance()

        # Da valor al tiempo medio entre interacciones 
    def set_mean_time_between_interaction(self):

        # Iniciamos una lista vacia donde se irá almacenando el tiempo entre interacciones.
        times_btw = []
        # Por cada uno de los eventos de la lista
        for index in range(len(self.events) - 1):
            # Se resta el tiempo del evento siguiente y del actual
            rest = int(self.events[index + 1]["start_datetime"]) - int(self.events[index]["start_datetime"])
            # El resto se almacena en la lista
            times_btw.append(rest)
        # Se calcula la media de la lista
        self.mean_time_between_interaction = statistics.mean(times_btw)

        # Se vacía la lista de tiempos
        times_btw = []
        for index in range(len(self.events_cleaned) - 1):
            rest = int(self.events_cleaned[index + 1]["start_datetime"]) - int(self.events_cleaned[index]["start_datetime"])
            times_btw.append(rest)
        self.mean_time_between_interaction_cleaned = statistics.mean(times_btw) 

    def set_total_distance(self):
        self.total_distance = 0.0
        for event in self.events:
            self.total_distance += event["distance"]

    def transform_dates(self):
        aux_list = []
        for event in self.events:
            event["start_datetime"] =  datetime.fromtimestamp(event["start_datetime"]).strftime("%Y-%m-%d %H:%M:%S")
            event["end_datetime"] =  datetime.fromtimestamp(event["end_datetime"]).strftime("%Y-%m-%d %H:%M:%S")
            aux_list.append(event)
        self.events = aux_list

    def get_results(self):
        results = super().get_results()
        results["total_distance"] = self.total_distance
        return results

    def get_results_for_global_analysis(self) -> dict:
        aux_dict = super().get_results_for_global_analysis()
        aux_dict["total_distance"] = self.total_distance

        return aux_dict