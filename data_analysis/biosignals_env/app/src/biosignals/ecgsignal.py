from biosppy.plotting import plot_ecg
from biosppy.signals import ecg
import matplotlib.pyplot as plt
import pandas as pd

from biosignals.biosignal import BioSignal


class ECGSignal(BioSignal):

    ecg_out_data: None

    def __init__(self, data) -> None:
        super().__init__(data)
        
        self.signals = [int(val) for val in list(self.df.iloc[:, 6])]
        self.analyse_signal()

    def analyse_signal(self):
        self.ecg_out_data = ecg.ecg(signal=self.signals, sampling_rate=self.data["hz"], show=False)
        self.filtered_signals = list(self.ecg_out_data[1])

    def plot_complex_data(self, filename):
        plot_ecg(
            ts = self.ecg_out_data[0], 
            raw = self.signals, 
            filtered = self.ecg_out_data[1],  
            rpeaks = self.ecg_out_data[2], 
            templates_ts = self.ecg_out_data[3], 
            templates = self.ecg_out_data[4], 
            heart_rate_ts = self.ecg_out_data[5], 
            heart_rate = self.ecg_out_data[6], 
            path=filename, 
            show=False)

    def plot_signal(self, x, y, filename):
        fig = plt.figure(figsize=(20, 2))

        plt.plot(x, y, linewidth=0.2)
        plt.title("ECG Summary")
        plt.xlabel("Time (s)")
        plt.ylabel("Heart Rate (bpm)")
        
        plt.tight_layout()
        plt.savefig(filename)