from models.events.Event import *

class MoveEvent(Event):
    '''
    Class MoveEvent
    -------------------

    La clase MoveEvent ...
    '''
#region VARIABLES GLOBALES
    
    move_type: str
    start_datetime: datetime
    end_datetime: datetime
    start_position: Vector2D
    end_position: Vector2D
    distance: float

#endregion

#region METODOS PUBLICOS
    
    def __init__(self, id:int = 0, user_id:int = 0, scenario_type:str = "",\
                 move_type:str = "", start_datetime:str="", end_datetime:str="", start_position:str="", end_position:str="", distance:float=0.0):
        super().__init__(id, user_id, scenario_type)

        self.move_type = move_type

        self.start_datetime = self.string_to_datetime(start_datetime)
        self.end_datetime = self.string_to_datetime(end_datetime)

        self.start_position = self.string_to_vector2d(start_position)
        self.end_position = self.string_to_vector2d(end_position)

        self.distance = distance

    
    def __repr__(self) -> None:
        return f'MoveEvent({self.id}, {self.user_id}, {self.scenario_type}, \
            {self.move_type}, {self.start_datetime}, {self.end_datetime}, {self.start_position}, {self.end_position}, {self.distance})'

    def __str__(self) -> None:
        return f'MoveEvent({self.id}, {self.user_id}, {self.scenario_type}, \
            {self.move_type}, {self.start_datetime}, {self.end_datetime}, {self.start_position}, {self.end_position}, {self.distance})'

#endregion
    
#region METODOS PRIVADOS
       

#enregion