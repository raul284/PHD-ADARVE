import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import time

from biosignals.ecgsignal import ECGSignal
from biosignals.edasignal import EDASignal

class User:
    id: str
    data: dict

    baseline_ecg: ECGSignal
    baseline_eda: EDASignal
    ingame_ecg: ECGSignal
    ingame_eda: EDASignal

    def __init__(self, id, data) -> None:
        self.id = id
        self.data = data

        # Baseline
        self.baseline_ecg = ECGSignal(self.data["baseline"])
        self.baseline_eda = EDASignal(self.data["baseline"])

        # In Game
        self.ingame_ecg = ECGSignal(self.data["ingame"])
        self.ingame_eda = EDASignal(self.data["ingame"])
        


    def create_graphs(self, ecg_lims, eda_lims):
        self.baseline_ecg.plot_complex_data("../results/{0}/baseline_ecg_{0}".format(self.id))
        self.baseline_eda.plot_complex_data("../results/{0}/baseline_eda_{0}".format(self.id))
        self.plot_joined_graph(
            [[x for x in range(len(self.baseline_ecg.ecg_out_data[1]))], [x for x in range(len(self.baseline_eda.eda_out_data[1]))]], 
            [self.baseline_ecg.ecg_out_data[1], self.baseline_eda.eda_out_data[1]], 
            "../results/{0}/baseline_{0}".format(self.id), 
            "Baseline Summary", ecg_lims, eda_lims)
        
        
        self.ingame_ecg.plot_complex_data("../results/{0}/ingame_ecg_{0}".format(self.id))
        self.ingame_eda.plot_complex_data("../results/{0}/ingame_eda_{0}".format(self.id))
        self.plot_joined_graph(
            [[x for x in range(len(self.ingame_ecg.ecg_out_data[1]))], [x for x in range(len(self.ingame_eda.eda_out_data[1]))]], 
            [self.ingame_ecg.ecg_out_data[1], self.ingame_eda.eda_out_data[1]], 
            "../results/{0}/ingame_{0}".format(self.id), 
            "In-game Summary", ecg_lims, eda_lims)

    def plot_joined_graph(self, x, y, filename, title, first_lims, second_lims):
        fig, axs = plt.subplots(2, 1, figsize=(20, 12))

        plt.xlabel("Time (s)")
        fig.suptitle(title)

        axs[0].plot(x[0], y[0], linewidth=0.2)
        axs[0].set_ylabel("Amplitude")
        axs[0].set_yticks(np.arange(first_lims[0], first_lims[1], step=100))

        axs[1].plot(x[1], y[1], linewidth=0.2)
        axs[1].set_ylabel("Amplitude")
        axs[1].set_yticks(np.arange(second_lims[0], second_lims[1], step=100))

        plt.tight_layout()
        plt.savefig(filename)
        #plt.show()