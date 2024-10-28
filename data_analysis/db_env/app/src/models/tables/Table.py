import os
import pandas as pd
from datetime import datetime
import statistics
import numpy as np
import re

from models.tables.ResultsTable import ResultsTable


class Table:

    _user_data: dict

    _table_name:str
    _df: pd.DataFrame
    _scenarios: dict

    _results: pd.DataFrame

    def __init__(self, user_data: dict, table_name: str) -> None:
        self.SCENARIOS = ["ALL", "T1", "S1", "T2", "S2"]

        self._user_data = user_data
        self._table_name = table_name

        self._df = pd.DataFrame()
        self._scenarios = {}

        self._results = pd.DataFrame()

    def set_data(self) -> None:
        self.read_data()
        self._df = self._df.set_index('id').reset_index(drop=True)
        #print(self._df.to_string())

        for scenario in self.SCENARIOS:
            self._scenarios[scenario] = self._df[self._df["scenario_type"] == scenario].reset_index()

    def get_cols_till(self, df):
        cols = []
        i = 0
        while df.columns[i] != "user_id":
            cols.append(df.columns[i])
            i += 1

        return cols

    def read_data(self) -> None:
        filename = self._table_name + "_events.csv"
        for dirpath, dirnames, filenames in os.walk("../data/"):
            for filename in [f for f in filenames if f == filename]:
                df = pd.read_csv(os.path.join(dirpath, filename))
                
                #df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                #df = df.shift(periods=1, axis="columns")
                #if not "id" in df:
                #    df.insert(0, "id", range(0, len(df)))
                if not "experiment_id" in df:
                    df.insert(2, "experiment_id", ["1" for x in range(len(df))])
                df.to_csv(os.path.join(dirpath, filename), index=False)
                self._df = pd.concat([self._df, df[(df["user_id"] == self._user_data["ID"]) & (df["experiment_id"] == self._user_data["EXP_ID"])]])

        self._df = self._df.replace("T1_BasicMechanics", "T1").replace("S1_BasicMechanics", "S1").replace("T2_BasicEmergency", "T2").replace("S2_BasicEmergency", "S2")

    def read_data_from_csv(self, filename) -> pd.DataFrame:
        df = pd.DataFrame()
        for dirpath, dirnames, filenames in os.walk("../data/"):
            for filename in [f for f in filenames if f == filename]:
                aux_df = pd.read_csv(os.path.join(dirpath, filename))
                df = pd.concat([df, aux_df[aux_df["user_id"] == self._user_data["ID"]]])

        return df
    
    def analyse_data(self) -> None:
        #print(self._df.to_string())
        if len(self._df) == 0:
            print("Usuario <<{0}>>. El DF de la tabla <<{1}>> está vacío".format(self._user_data["ID"], self._table_name))

        results = {}
        print("################ ALL")
        results["ALL"] = {**self._user_data, **{"SCENARIO": "ALL"}, **self.analyse_df(self._df.copy())}
        
        for scenario in self.SCENARIOS[1:]:
            print("################ {}".format(scenario.upper()))
            if not self._scenarios[scenario].empty:
                results[scenario] = {**self._user_data, **{"SCENARIO": scenario}, **self.analyse_df(self._scenarios[scenario].copy())}
            else: 
                results[scenario] = {**self._user_data, **{"SCENARIO": scenario}}


        self._results = pd.DataFrame.from_records(list(results.values()))

    def analyse_df(self, df) -> dict:
        return {**self.analyse_number(df), **self.analyse_time(df)}
    
    def analyse_number(self, df) -> dict:
        return {}

    def analyse_time(self, df) -> dict:
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
        #print(datetimes_list)
        #print("==================", round(statistics.mean(times_btw), 2))

        # Se calcula la media de la lista
        if times_btw: return round(statistics.mean(times_btw) / 1000, 3)
        else: 0.0
    
    def get_time_btw_two_type(self, fst_df, snd_df):
        return np.nan

        

#endregion