import pandas as pd
from datetime import datetime
from typing import TypeVar, Generic, Type
import matplotlib.pyplot as plt

from models.tables.ResultsTable import ResultsTable

T = TypeVar('T')

class Table(Generic[T]):

    _df: pd.DataFrame
    _results: ResultsTable

    def __init__(self, generic_type: Type[T]) -> None:
        self._generic_type = generic_type
        self._list: list[self._generic_type] = []

    def read_data_from_csv(self, filename: str) -> None:
        self._df = pd.read_csv("../data/{0}.csv".format(filename))
        self._list = [self._generic_type(*row.to_list()) for index, row in self._df.iterrows()]

    def get_data_list_by_user(self, user_id: int) -> list:
        return [event for event in self._list if event.user_id == user_id]

    def get_data_dataframe_by_user(self, user_id: int) -> pd.DataFrame:
        return self._df[self._df["user_id"] == user_id]
    
    def analyse_data(self):
        self._results.analyse_data()

    def get_results(self):
        return self._results._df

    def export_results(self):
        self._results.export_results()

    def create_graphs(self):
        pass

#region METODOS PRIVADOS
       

    def string_to_datetime(self, s_datetime) -> datetime:
        return datetime.strptime(s_datetime, '%Y-%m-%d %H:%M:%S')

#enregion