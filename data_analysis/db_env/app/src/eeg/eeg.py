import pyxdf
import os
import matplotlib.pyplot as plt
import numpy as np


class EEG:

    _filename: str

    def __init__(self) -> None:
        self._filename = "../data/eeg.xdf"
        # Check if the file exists
        if not os.path.exists(self._filename):
            print(f"File {self._filename} not found.")
        else:
            # Load the XDF file
            data, header = pyxdf.load_xdf(self._filename)

            print(data)

            # Iterate through the loaded streams
            for stream_index, stream in enumerate(data, start=1):
                print(f"Stream {stream_index}: {stream['info']['name'][0]}")
                channel_count = int(stream['info']['channel_count'][0])
                channel_labels = [f"Channel {i+1}" for i in range(channel_count)]
                
                # Assuming time_series is a 2D array (channels x samples). Transpose if necessary.
                time_series = np.array(stream['time_series'])
                if time_series.ndim == 2 and time_series.shape[0] < time_series.shape[1]:
                    time_series = time_series.T  # Make sure it's samples x channels
                
                # Time stamps
                time_stamps = np.array(stream['time_stamps'])
                if time_stamps.size == 0:  # If no time stamps, generate based on sampling rate
                    time_stamps = np.arange(time_series.shape[0])
                
                fig, axs = plt.subplots(channel_count, 1, figsize=(10, 18), layout='tight', sharex=True, sharey=True)

                # Plot each channel
                for i in range(channel_count):
                    axs[i].plot(time_stamps, time_series[:, i])
                    axs[i].title.set_text(f"{stream['info']['name'][0]} - {channel_labels[i]}")

                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')

                #plt.show()