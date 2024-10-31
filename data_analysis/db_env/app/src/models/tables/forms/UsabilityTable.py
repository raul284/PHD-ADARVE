import pandas as pd

from models.tables.forms.Table import Table
from models.form.Usability import Usability

class UsabilityTable(Table):

    def __init__(self, user_id: str, data:pd.DataFrame) -> None:
        super().__init__(user_id, data)
    
    def set_data(self):
        return super().set_data()
    
    def analyse_data(self) -> None:
        sus = Usability(self._df)
        sus.calculate()
        self._results = sus.get_results()
        
    def get_results(self):
        return super().get_results()

    def export_results(self):
        return super().export_results()

    def create_graphs(self):
        return super().create_graphs()

#region METODOS PRIVADOS

#endregion