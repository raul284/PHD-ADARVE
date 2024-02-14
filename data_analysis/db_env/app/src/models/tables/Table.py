import pandas as pd
from datetime import datetime

from models.tables.ResultsTable import ResultsTable


class Table:

    _table_name:str
    _df: pd.DataFrame
    _results: ResultsTable

    def __init__(self, table_name: str) -> None:
        self._table_name = table_name.upper()

    def read_data_from_csv(self, filename: str) -> None:
        self._df = pd.read_csv("../data/{0}.csv".format(filename))
        self.clean_initial_dataframe()

    def get_data_by_user(self, user_id: int) -> pd.DataFrame:
        return self._df[self._df["ID"] == user_id]
    
    def analyse_data(self):
        self._results.analyse_data()

    def get_results(self):
        return self._results._df

    def export_results(self):
        self._results.export_results()

    def create_graphs(self):
        pass

#region METODOS PRIVADOS
       
    def clean_initial_dataframe(self):
        pass

    def string_to_datetime(self, s_datetime) -> datetime:
        return datetime.strptime(s_datetime, '%Y-%m-%d %H:%M:%S')
    
    def set_id_column(self) -> None:
        if "user_id" in self._df.columns:
            self._df.drop("id", inplace=True, axis=1)
            self._df.rename(columns={"user_id": "ID"}, inplace=True)
        

#enregion