import statistics
from datetime import datetime
import pandas as pd


class Events:

    # Listado de todos los eventos
    events: pd.DataFrame

    # Listado de todos los eventos sin repeticiones. Se consideran repetidos aquellos 
    # eventos que sean el mismo y que se hayan producido en el mismo segundo.
    events_cleaned: pd.DataFrame

    # Numero de interacciones totales, es decir, el número de eventos. Con repeticiones y sin repeticiones
    num_of_interactions: int
    num_of_interactions_cleaned: int

    # Tiempo medio entre interacciones. Con y sin repeticiones.
    mean_time_between_interaction: float
    mean_time_between_interaction_cleaned: float


    def __init__(self, raw_data) -> None:
        self.events = raw_data
        self.events_cleaned = self.remove_duplicate(self.events)


    def analyse_data(self) -> None:
        self.set_num_of_interactions()
        self.set_mean_time_between_interaction()

    # Elimina las repeticiones de la lista.
    def remove_duplicate(self, events: pd.DataFrame):
        '''result = []

        # Recorre toda la lista de eventos
        for event in events:
            # En el caso de que el evento no esté en la lista, lo añade
            if event not in result:
                result.append(event)'''

        return events.drop_duplicates()

    def get_event_of_type(self, event_type):
        for event in self.events:
            if event["event_type"] == event_type:
                return event
            
    def get_first_event_of_type(self, event_type):
        return self.events.loc[self.events["event_type"] == event_type].iloc[0]
        '''aux_events = []
        for event in self.events:
            if event["event_type"] == event_type:
                aux_events.append(event)
        return aux_events[0]'''
            
    def get_last_event_of_type(self, event_type):
        return self.events.loc[self.events["event_type"] == event_type].iloc[-1]
        '''aux_events = []
        for event in self.events:
            if event["event_type"] == event_type:
                aux_events.append(event)
        return aux_events[-1]'''


    # Da valor al número de interacciones
    def set_num_of_interactions(self):
        self.num_of_interactions = len(self.events)
        self.num_of_interactions_cleaned = len(self.events_cleaned)

    # Da valor al tiempo medio entre interacciones 
    def set_mean_time_between_interaction(self):

        # Iniciamos una lista vacia donde se irá almacenando el tiempo entre interacciones.
        times_btw = []
        # Por cada uno de los eventos de la lista
        for index in range(len(self.events) - 1):
            # Se resta el tiempo del evento siguiente y del actual
            rest = int(self.events.iloc[[index + 1]]["event_datetime"]) - int(self.events.iloc[[index]]["event_datetime"])
            # El resto se almacena en la lista
            times_btw.append(rest)
        # Se calcula la media de la lista
        if len(times_btw) > 0:
            self.mean_time_between_interaction = statistics.mean(times_btw)

        # Se vacía la lista de tiempos
        times_btw = []
        for index in range(len(self.events_cleaned) - 1):
            rest = int(self.events_cleaned.iloc[[index + 1]]["event_datetime"]) - int(self.events_cleaned.iloc[[index]]["event_datetime"])
            times_btw.append(rest)
        if len(times_btw) > 0:
            self.mean_time_between_interaction_cleaned = statistics.mean(times_btw)       

    def transform_dates(self):
        aux_list = []
        for event in self.events:
            event["event_datetime"] =  datetime.fromtimestamp(event["event_datetime"]).strftime("%Y-%m-%d %H:%M:%S")
            aux_list.append(event)
        self.events = aux_list

    def get_results(self):
        return {
            #"raw": self.events.to_dict(),
            #"cleaned": self.events_cleaned.to_dict(),
            "numOfInteractions": {
                "with_rep": self.num_of_interactions,
                "without_rep": self.num_of_interactions_cleaned,
            },
            "meanTimeBetweenInteraction":{
                "with_rep": self.mean_time_between_interaction,
                "without_rep": self.mean_time_between_interaction_cleaned,
            }
        }
    
    def get_results_for_global_analysis(self) -> dict:
        return {
            "numOfInteractions": {
                "with_rep": self.num_of_interactions,
                "without_rep": self.num_of_interactions_cleaned,
            },
            "meanTimeBetweenInteraction":{
                "with_rep": self.mean_time_between_interaction,
                "without_rep": self.mean_time_between_interaction_cleaned,
            }
        }

    


