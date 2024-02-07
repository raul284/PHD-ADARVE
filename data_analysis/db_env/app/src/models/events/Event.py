from datetime import datetime
from structs.Vector2D import Vector2D

class Event:
    '''
    Class Event
    -------------------

    La clase Event ...
    '''
#region VARIABLES GLOBALES

    id: int
    user_id: int
    scenario_type: str

#endregion

#region METODOS PUBLICOS
    
    def __init__(self, id:int = 0, user_id:int = 0, scenario_type:str = "") -> None:

        self.id = id
        self.user_id = user_id
        self.scenario_type = scenario_type

    # __init__

    def __repr__(self) -> None:
        return f'Event({self.id}, {self.user_id}, {self.scenario_type})'

    def __str__(self) -> None:
        return f'Event({self.id}, {self.user_id}, {self.scenario_type})'
    
    def transform_dates(self) -> None:
        pass

#endregion
    
#region METODOS PRIVADOS
    def string_to_datetime(self, s_datetime) -> datetime:
        return datetime.strptime(s_datetime, '%Y-%m-%d %H:%M:%S')
    
    def string_to_vector2d(self, s_vector) -> Vector2D:
        vector = s_vector[1:-1].split(";")
        return Vector2D(float(vector[0]), float(vector[1]))
#enregion
