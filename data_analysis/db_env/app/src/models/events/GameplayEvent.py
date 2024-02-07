from models.events.Event import *

class GameplayEvent(Event):
    '''
    Class GameplayEvent
    -------------------

    La clase GameplayEvent ...
    '''
#region VARIABLES GLOBALES
    
    event_state: str
    event_type: str
    event_datetime: datetime
    
#endregion

#region METODOS PUBLICOS
    
    def __init__(self, id:int = 0, user_id:int = 0, scenario_type:str = "",\
                 event_state:str = "", event_type:str="", event_datetime:str=""):
        super().__init__(id, user_id, scenario_type)

        self.event_state = event_state
        self.event_type = event_type
        self.event_datetime = self.string_to_datetime(event_datetime)

    
    def __repr__(self) -> None:
        return f'GameplayEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.event_state}, {self.event_type}, {self.event_datetime})'

    def __str__(self) -> None:
        return f'GameplayEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.event_state}, {self.event_type}, {self.event_datetime})'

#endregion
    
#region METODOS PRIVADOS
       

#enregion