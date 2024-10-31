import pandas as pd

class CognitiveLoad():
    '''
    Class CognitiveLoad
    ----------------------------------------
    Clase que gestiona el cálculo de la carga cognitiva. Para ello se está utilizando el NASA-TLX (https://humansystems.arc.nasa.gov/groups/tlx/downloads/TLXScale.pdf).
    
    Este cuestionario está formado por 6 rasgos:
    - Mental Demand:
    - Physical Demand:
    - Temporal Demand:
    - Effort:
    - Performance:
    - Frustration:

    El cuestionario está compuesto por un total de 6 preguntas con escala likert [1, 10] (una por cada factor). Además, tiene una fase previa donde al usuario se le 
    pregunta 'qué factor considera más importante' para así calcular los pesos. Por ejemplo, al usuario se le plantea "Consideras que la tarea 
    ha tenido más Exigencias Mentales o Rendimiento.
    
    Los pesos se calculan sumando el número de veces que el usuario ha seleccionado cada factor dividido entre 15. Por ejemplo, si el usuario ha 
    dicho que la tarea ha supuesto más Exigencia Física un total de 5 veces sería Peso(Exigencia Física) = 5 / 15

    El cálculo de cada factor se hace multiplicando la respuesta de la pregunta de ese factor por el peso de dicho factor. La puntuación total se calcula sumando todas.
    
    '''

    _data: pd.DataFrame
    _results: dict

    _scores: dict   # Guarda los resultados de cada uno de los factores. Podría ponerse directamente en self._results, 
                    # pero por comodidad lo hago en una variable a parte.
    _weights: dict  # Guarda los resultados de los pesos de cada factor.

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._results = {}

        # Inicializa el dict con el valor 0 por cada factor
        self._scores = {
            "CL_MD": 0.0,   # Mental Demand
            "CL_PD": 0.0,   # Physical Demand
            "CL_TD": 0.0,   # Temporal Demand
            "CL_E": 0.0,    # Effort
            "CL_P": 0.0,    # Performance
            "CL_F": 0.0     # Frustration
        }

        # Inicializa el dict con el valor 0 por cada factor. Lo que hago es inicializarlo igual que self._scores pero a cada key le añado _W_ 
        # que indica que es el peso. Ahora mismo no tiene mucho sentido esto. Sin embargo, al final se concatenarán _scores y _weights. De 
        # esta manera ya está preparado para que no se pisen los valores entre ellos.
        self._weights = {key.replace("_", "_W_"): 0.0 for key in self._scores}


    def calculate(self):
        user_responses_weights = self._data.iloc[:, 0:15]
        user_responses_scores = self._data.iloc[:, 15:].values[0]

        # Se calculan los pesos
        for col in user_responses_weights.columns:
            # Esto es algo que hago porque los datos provienen de un excel que Google Form. Cada pregunta en Google Form es como la siguiente:
            #
            #     -----------------------------------------------------------------------------------------------------------------------------------------------
            #     |  Pregunta: [S-CL] Teniendo en cuenta las definiciones anteriores. ¿Cuál aspecto del par presentado contribuye más a la carga de la tarea?   |
            #     |  Selecciona una de las dos opciones presentadas de cada pareja: [Exigencias Mentales / Exigencias Físicas]                                  |
            #     |                                                                                                                                             |
            #     |  Respuestas: Primera opción ó Segunda opción                                                                                                |
            #     -----------------------------------------------------------------------------------------------------------------------------------------------
            # 
            # La variable <<options>> guardará dos valores. Teniendo en cuenta el ejemplo, sería [Exigencias Mentales, Exigencias Físicas]
            options = col.split("[")[-1].split("]")[0].split(" / ")
            # Si la respuesta es "Primera opción" (por eso compruebo si contiene <<Primera>>) entonces la opción seleccionada es <<Exigencias Mentales>>
            selected = options[0] if "Primera" in user_responses_weights.iloc[0].at[col] else options[1]

            # Hacemos un switch y sumamos 1 al peso del factor que corresponda
            if selected == "Exigencias Mentales":
                self._weights["CL_W_MD"] += 1
            elif selected == "Exigencias Físicas":
                self._weights["CL_W_PD"] += 1
            elif selected == "Exigencias Temporales":
                self._weights["CL_W_TD"] += 1
            elif selected == "Esfuerzo":
                self._weights["CL_W_E"] += 1
            elif selected == "Rendimiento":
                self._weights["CL_W_P"] += 1
            elif selected == "Nivel de Frustración":
                self._weights["CL_W_F"] += 1
        
        # Dividimos entre 15 cada uno de los pesos. ¿Se podría hacer en una línea? Sí, pero me entre que no me fío de Python y menos de mí mismo, prefiero usar variables auxiliares.
        for w in self._weights:
            aux = self._weights[w] / 15
            self._weights[w] = aux
            # Aquí ya nos guardamos los pesos en self._results. Se podría hacer después, pero ya que estoy...
            self._results[w] = round(aux, 3)

        response_index = 0
        # Se calculan las puntuaciones multiplicando las puntuaciones del usuario con los pesos.
        for key in self._scores:
            self._scores[key] = float(round(user_responses_scores[response_index] * self._weights[key.replace("_", "_W_")], 3))
            response_index += 1
        
        # Se añaden las puntuaciones a los resultados
        self._results = {**self._results, **self._scores}
        # Cálculo de la puntuación final
        self._results["CL_SCORE"] = round(sum(self._results.values()), 3)

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self._results, index=[0])