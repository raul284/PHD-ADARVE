import pandas as pd

class Table:

    _user_id: str

    _df: pd.DataFrame
    _results: pd.DataFrame

    def __init__(self, user_id: str, data: pd.DataFrame) -> None:
        self._user_id = user_id
        
        self._df = data
        self._results = pd.DataFrame()

    def set_data(self) -> None:
        pass
    
    def analyse_data(self) -> None:
        pass
        
    def get_results(self):
        return pd.concat([pd.DataFrame({"ID": [self._user_id]}), self._results], axis=1)

    def export_results(self):
        pass

    def create_graphs(self):
        pass

#region METODOS PRIVADOS
        

#endregion