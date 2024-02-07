from models.events.Event import *

class TemplateEvent(Event):
    '''
    Class TemplateEvent
    -------------------

    La clase TemplateEvent ...
    '''
#region VARIABLES GLOBALES
    
    template_var: int
    
#endregion

#region METODOS PUBLICOS
    
    def __init__(self, id:int = 0, user_id:int = 0, scenario_type:str = "",\
                 template_var: int = 0):
        super().__init__(id, user_id, scenario_type)

        self.template_var = template_var

    
    def __repr__(self) -> None:
        return f'TemplateEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.template_var} )'

    def __str__(self) -> None:
        return f'TemplateEvent({self.id}, {self.user_id}, {self.scenario_type}, {self.template_var})'

#endregion
    
#region METODOS PRIVADOS
       

#enregion