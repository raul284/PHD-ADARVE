from models.events.Event import *

class UserInputEvent(Event):
    '''
    Class UserInputEvent
    -------------------

    La clase UserInputEvent ...
    '''
#region VARIABLES GLOBALES
    
    input_type: str
    input_state: str
    event_datetime: str
    
#endregion

#region METODOS PUBLICOS
    
    def __init__(self, id:int = 0, user_id:int = 0, scenario_type:str = "",\
                 input_type:str="", input_state:str="", event_datetime:str=""):
        super().__init__(id, user_id, scenario_type)

        self.input_type = input_type
        self.input_state = input_state
        self.event_datetime = event_datetime

    
    def __repr__(self) -> None:
        return f'UserInputEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.input_type}, {self.input_state}, {self.event_datetime} )'

    def __str__(self) -> None:
        return f'UserInputEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.input_type}, {self.input_state}, {self.event_datetime} )'

#endregion
    
#region METODOS PRIVADOS
       

#enregion