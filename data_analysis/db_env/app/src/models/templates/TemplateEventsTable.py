from models.tables.Table import *

class TemplateEventsTable(Table[T]):
    '''
    Class TemplateEventsTable
    -------------------

    La clase TemplateEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, generic_type: Type[T]) -> None:
        super().__init__(generic_type=generic_type)

    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)
        
#endregion
    
#region METODOS PRIVADOS
       

#enregion