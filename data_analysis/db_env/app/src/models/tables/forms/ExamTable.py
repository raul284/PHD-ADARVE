import pandas as pd

from models.tables.forms.Table import Table
from models.form.Exam import Exam

class ExamTable(Table):
    _score: int

    def __init__(self, user_id: str, data:pd.DataFrame, score:int) -> None:
        super().__init__(user_id, data)
        self._score = score
    
    def set_data(self):
        return super().set_data()
    
    def analyse_data(self) -> None:
        exam = Exam(self._df)
        exam.analyse_data()
        self._results = exam.get_results()
        self._results = pd.concat([self._results, pd.DataFrame({"S-APP-SCORE": [self._score]})], axis=1)
        
    def get_results(self):
        return super().get_results()

    def export_results(self):
        return super().export_results()

    def create_graphs(self):
        return super().create_graphs()
    
    def change_results_columns_prefix(self, new_sufix):
        self._results = self._results.rename(columns={col: col.replace("S-APP-", new_sufix) for col in self._results.columns})

#region METODOS PRIVADOS

#endregion