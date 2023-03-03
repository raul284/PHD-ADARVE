import pandas as pd

class BioSignal:

    data: dict
    df: pd.DataFrame
    signals: list
    filtered_signals: list

    def __init__(self, data) -> None:
        self.data = data
        self.df = self.data["signal"]

    def analyse_signal(self):
        pass

    def plot_complex_data(self, filename):
        pass 

    def plot_signal(self, x, y, filename):
        pass