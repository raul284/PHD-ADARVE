import os
import pandas as pd
from datetime import datetime
import statistics
import numpy as np

from models.tables.ResultsTable import ResultsTable


class Table:

    _user_data: dict

    _table_name:str
    _df: pd.DataFrame
    _scenarios: dict

    _results: pd.DataFrame

    def __init__(self, user_data: dict, table_name: str) -> None:
        self._user_data = user_data
        self._table_name = table_name

        self._df = pd.DataFrame()
        self._scenarios = {}

        self._results = pd.DataFrame()

    def set_data(self) -> None:
        self.read_data_from_csv()

        for scenario in self._df["scenario_type"].unique():
            self._scenarios[scenario] = self._df[self._df["scenario_type"] == scenario]

    def read_data_from_csv(self) -> None:
        filename = self._table_name + "_events.csv"
        for dirpath, dirnames, filenames in os.walk("../data/"):
            for filename in [f for f in filenames if f == filename]:
                df = pd.read_csv(os.path.join(dirpath, filename))
                self._df = pd.concat([self._df, df[df["user_id"] == self._user_data["ID"]]])

        self.clean_initial_dataframe()
    
    def analyse_data(self) -> None:
        if len(self._df) == 0:
            print("Usuario <<{0}>>. El DF de la tabla <<{1}>> está vacío".format(self._user_data["ID"], self._table_name))

        results = {}

        results["ALL"] = {**self._user_data, **{"SCENARIO": "ALL"}, **self.analyse_df(self._df)}
        
        for scenario in self._df["scenario_type"].unique():
            results[scenario] = {**self._user_data, **{"SCENARIO": scenario}, **self.analyse_df(self._scenarios[scenario])}

        self._results = pd.DataFrame.from_records(list(results.values()))

    def analyse_df(self, df) -> dict:
        return {}
        
    def get_results(self):
        if len(self._results) > 0: return self._results
        else: return pd.DataFrame()
    
    def get_results_by_scenario(self, scenario_type):
        results = self._results[self._results["SCENARIO"] == scenario_type]
        if len(results) > 0: return results
        else: return pd.DataFrame()

    def export_results(self):
        pass
        #self._results.export_results()

    def create_graphs(self, path, lims):
        pass
        #self.create_graphs_for_eeg(path, lims)

    def create_graphs_for_eeg(self, path, lims):
        pass

#region METODOS PRIVADOS
       
    def clean_initial_dataframe(self):
        self._df = self._df.replace("T1_BasicMechanics", "T1").replace("S1_BasicMechanics", "S1").replace("T2_BasicEmergency", "T2").replace("S2_BasicEmergency", "S2")

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
        #print(datetimes_list)
        #print("==================", round(statistics.mean(times_btw), 2))

        # Se calcula la media de la lista
        return round(statistics.mean(times_btw) / 1000, 2)

        

#endregion