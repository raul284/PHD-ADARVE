import os
import pandas as pd
from datetime import datetime
import statistics
import numpy as np
import re

class Table:

    _user_data: dict

    _table_name:str
    _df: pd.DataFrame
    _data: dict

    _results: pd.DataFrame

    def __init__(self, user_data: dict, table_name: str) -> None:
        self._user_data = user_data
        self._table_name = table_name

        self._df = pd.DataFrame()
        self._data = {}
        self._results = pd.DataFrame()

    def set_data(self, filename) -> None:
        self.read_data(filename)
        #self._df = self._df.set_index('id').reset_index(drop=True)
        self._data["pd"] = self._df[[col for col in self._df.columns if "S-PD" in col]]
        self._data["app"] = self._df[[col for col in self._df.columns if "S-APP" in col]]
        self._data["ux"] = self._df[[col for col in self._df.columns if "S-UX" in col]]
        self._data["sus"] = self._df[[col for col in self._df.columns if "S-SUS" in col]]
        self._data["cl"] = self._df[[col for col in self._df.columns if "S-CL" in col]]

    def read_data(self, filename) -> None:
        self._df = pd.read_excel("../data/{0}".format(filename))
        id_col_name = [col for col in self._df.columns if "[ID]" in col][0]
        self._df = self._df[self._df[id_col_name] == self._user_data["ID"]]
        #self._df = pd.concat([self._df, df[(df["user_id"] == self._user_data["ID"]) & (df["experiment_id"] == self._user_data["EXP_ID"])]])
    
    def analyse_data(self) -> None:
        results = {}
        results["app"] = self.analyse_app()
        results["ux"] = self.analyse_ux()
        results["sus"] = self.analyse_sus()
        results["cl"] = self.analyse_cl()

        self._results = pd.DataFrame([results])
        print(self._results)

    def analyse_app(self) -> float:
        result = 0.0
        df = self._data["app"]

        return result
    
    def analyse_ux(self) -> dict:
        result = {}
        df = self._data["ux"]

        ids = {
            "attractiveness": [0, 11, 13, 15, 23, 24],
            "perspicuity": [1, 3, 12, 20],
            "efficiency": [8, 19, 21, 22],
            "dependability": [7, 10, 16, 18],
            "stimulation": [4, 5, 6, 17],
            "novelty": [2, 9, 14, 25]
        }

        for trait in ids:
            result[trait[0]] = round(sum([df[df.columns[id]] - 4 for id in ids[trait]]) / len(ids[trait]), 3)

        return result
    
    def analyse_sus(self) -> float:
        result = 0.0
        df = self._data["sus"]
        
        # X se calcula con los números impares e Y con los pares
        # Para coger los valores pares e impares estoy lo estoy haciendo a la inversa
        # Los índices pares en programación serían el 0, 2, 4...pero en la vida real esto es 1, 2, 5...
        # Por ello, estoy pillando los índices al contrario.
        x = sum([df[col] for col in df.columns[::2]]) - 5.0
        y = 25.0 - sum([df[col] for col in df.columns[1::2]])
        result = (x + y) * 2.5

        return result
    
    def analyse_cl(self) -> float:
        df = self._data["cl"]

        result = {
            "mental_demand": 0,
            "physical_demand": 0,
            "temporal_demand": 0, 
            "effort": 0,
            "performance": 0,
            "frustration": 0
        }
        weights = result.copy()

        weight_df = df.iloc[:, 0:15]
        for col in weight_df.columns:
            options = col.split("[")[-1].split("]")[0].split(" / ")
            selected = options[0] if "Primera" in weight_df.iloc[0].at[col] else options[1]

            match selected:
                case "Exigencias Mentales":
                    weights["mental_demand"] += 1
                case "Exigencias Físicas":
                    weights["physical_demand"] += 1
                case "Exigencias Temporales":
                    weights["temporal_demand"] += 1
                case "Esfuerzo":
                    weights["effort"] += 1
                case "Rendimiento":
                    weights["performance"] += 1
                case "Nivel de Frustración":
                    weights["frustration"] += 1
            
        for w in weights:
            aux = weights[w] / 15
            weights[w] = aux

        scores = df.iloc[:, 15:].values[0]
        score_index = 0

        for key in result:
            result[key] = scores[score_index] * weights[key]
            score_index += 1

        cl_score = round(sum(result.values()), 3)
        print(cl_score)

        return result
        
    def get_results(self):
        if len(self._results) > 0: return self._results
        else: return pd.DataFrame()

    def export_results(self):
        pass

    def create_graphs(self, path, lims):
        pass

#region METODOS PRIVADOS
    def fix_datetimes(self, df) -> list:
        datetime_list = []
        for date in list(df):
            splitted_date = re.split('-|:| |\.', date)
            for i in range(1, 6):
                splitted_date[i] = splitted_date[i].zfill(2)
            splitted_date[6] = splitted_date[6].zfill(3)
            datetime_list.append("{0}-{1}-{2} {3}:{4}:{5}.{6}".format(*splitted_date))

        return datetime_list
        #pd.to_datetime(df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")

    def string_to_datetime(self, s_datetime) -> datetime:
        return datetime.strptime(s_datetime, '%Y-%m-%d %H:%M:%S.%f')
    
    def set_id_column(self) -> None:
        if "user_id" in self._df.columns:
            self._df.drop("id", inplace=True, axis=1)
            self._df.rename(columns={"user_id": "ID"}, inplace=True)

    def get_time_btw_datetimes(self, datetimes_list) -> float:
        # Iniciamos una lista vacia donde se irá almacenando el tiempo entre interacciones.
        times_btw = []
        # Por cada uno de los eventos de la lista
        for index in range(len(datetimes_list) - 1):
            # Se resta el tiempo del evento siguiente y del actual
            rest = int(datetimes_list[index + 1].timestamp() * 1000) - int(datetimes_list[index].timestamp() * 1000)
            # El resto se almacena en la lista
            times_btw.append(rest)

        # Se calcula la media de la lista
        if times_btw: return round(statistics.mean(times_btw) / 1000, 3)
        else: 0.0
    
    def get_time_btw_two_type(self, fst_df, snd_df, filters):
        time_btw = []

        while not fst_df.empty and not snd_df.empty:
            first_event = fst_df.iloc[0]

            if filters:
                potential_snd_events = None
                for f in filters:
                    potential_snd_events = snd_df[snd_df[f] == first_event[f]]
                
                snd_index = potential_snd_events.index[0]
                snd_event = potential_snd_events.iloc[0]

            else:
                snd_index = snd_df.index[0]
                snd_event = snd_df.iloc[0]
            
            time = self.get_time_btw_datetimes([first_event["event_datetime"], snd_event["event_datetime"]])
            if time < 0: print("Hay un tiempo entre interacciones negativo.")

            time_btw.append(time)

            fst_df = fst_df.iloc[1:]
            snd_df = snd_df.drop(snd_index)

        if len(time_btw) > 0: return statistics.mean(time_btw)
        else: return np.nan

        

#endregion