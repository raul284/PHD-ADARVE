from models.events.Event import *

class TipsEvent(Event):
    '''
    Class TipsEvent
    -------------------

    La clase TipsEvent ...
    '''
#region VARIABLES GLOBALES
    
    tip_type: str
    event_datetime: str
    
#endregion

#region METODOS PUBLICOS
    
    def __init__(self, id:int = 0, user_id:int = 0, \
                 tip_type:str="", event_datetime:str=""):
        super().__init__(id, user_id, "")

        self.tip_type = tip_type
        self.event_datetime = event_datetime

    
    def __repr__(self) -> None:
        return f'TipsEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.tip_type}, {self.event_datetime} )'

    def __str__(self) -> None:
        return f'TipsEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.tip_type}, {self.event_datetime})'

#endregion
    
#region METODOS PRIVADOS
       

#enregion