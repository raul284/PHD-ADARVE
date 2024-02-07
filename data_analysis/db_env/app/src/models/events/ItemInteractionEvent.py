from models.events.Event import *

class ItemInteractionEvent(Event):
    actor_id: int
    event_type: str
    event_datetime: datetime

    def __init__(self, id:int = 0, user_id:int = 0, scenario_type:str = "",\
                 actor_id:int = 0, event_type:str="", event_datetime:str=""):
        super().__init__(id, user_id, scenario_type)

        self.actor_id = actor_id
        self.event_type = event_type
        self.event_datetime = self.string_to_datetime(event_datetime)

    def __repr__(self):
        return f'ItemInteractionEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.actor_id}, {self.event_type}, {self.event_datetime})'

    def __str__(self):
        return f'ItemInteractionEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.actor_id}, {self.event_type}, {self.event_datetime})'