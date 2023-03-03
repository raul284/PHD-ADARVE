import statistics


class FieldStatistics:
    '''
    Class FieldStatistics
    -------------------

    Clase que realiza los principales calculos estadisticos para una lista de valores. Actualmente calcula
    la media y la desviacion estandar de la lista de valores. 

    Permite añadir nuevos valores a esta lista y devuelve la informacion en forma de diccionario.
    '''

#region VARIABLES GLOBALES
 
    # Lista de los valores sobre los que se quieren realizar los calculos
    values: list

    # La media de los valores
    mean: float

    # La desviacion estandar de los valores
    stdev: float

#endregion

#region METODOS

    def __init__(self) -> None:
        '''Inicializa las propiedades de la clase.'''

        # Iniciacion de los valores
        self.values = []
        self.mean = 0.0
        self.stdev = 0.0

    # __init__


    def add_values(self, values: list) -> None:
        '''
        Añade nuevos valores a la lista y hace los calculos que la lista completa.

        :param values: Nuevos valores
        '''

        # Añade valores a la lista
        self.values += values

        # Calcula los resultados
        self.mean = statistics.mean(self.values) if (len(self.values) > 1) else self.values[0]
        self.stdev = statistics.stdev(self.values) if (len(self.values) > 1) else self.values[0]

    # add_values


    def get_statistics(self) -> dict:
        '''
        Devuelve los resultados en forma de diccionario.

        :return: diccionario con los resultados
        '''

        return {
            "mean": self.mean,
            "stdev": self.stdev
        }
    
    # get_statistics

#endregion
    
        
