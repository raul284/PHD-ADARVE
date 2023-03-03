from biosppy.plotting import plot_eda
from biosppy.signals import eda
import matplotlib.pyplot as plt

from biosignals.biosignal import BioSignal


class EDASignal(BioSignal):

    eda_out_data: None

    def __init__(self, data) -> None:
        super().__init__(data)

        self.signals = [int(val) for val in list(self.df.iloc[:, 7])]
        self.analyse_signal()

    def analyse_signal(self):
        self.eda_out_data = eda.eda(signal=self.signals, sampling_rate=100.0, show=False)
        self.filtered_signals = list(self.eda_out_data[1])

    def plot_complex_data(self, filename):
        plot_eda(
            ts = self.eda_out_data[0], 
            raw = self.signals, 
            filtered = self.eda_out_data[1], 
            onsets = self.eda_out_data[2], 
            peaks = self.eda_out_data[3], 
            amplitudes = self.eda_out_data[4], 
            path=filename, 
            show=False)

    def plot_signal(self, x, y, filename):
        fig = plt.figure(figsize=(20, 2))

        plt.plot(x, y, linewidth=0.3)
        plt.title("EDA Summary")
        plt.xlabel("Time (s)")
        plt.ylabel("Heart Rate (bpm)")

        plt.tight_layout()
        plt.savefig(filename)