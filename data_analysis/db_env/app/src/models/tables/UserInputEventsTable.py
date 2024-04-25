from enums.E_UserInputType import UserInputType

from models.tables.Table import *

class UserInputEventsTable(Table):
    '''
    Class UserInputEventsTable
    -------------------

    La clase UserInputEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, table_name:str="") -> None:

        super().__init__(table_name=table_name)

        self._results = ResultsTable(["UI_NUM"] + \
                                     ["UI_NUM_TYPE_{0}".format(index.name) for index in UserInputType] + \
                                     ["UI_TIME"])


    def read_data_from_csv(self, filename: str) -> None:
        super().read_data_from_csv(filename)

        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        

    def analyse_data(self):
        super().analyse_data()

        aux_results = {
            "UI_NUM": float(len(self._df)),
            "UI_NUM_GP_STEPS": 0.0,
            "UI_TIME": self._results.get_time_btw_datetimes(self._df["event_datetime"].to_list())
        }

        for index in UserInputType:
            aux_results["UI_NUM_TYPE_{0}".format(index.name)] = float(len(self._df[self._df["input_type"].str.upper() == index.name]))

        self._results.insert_row(aux_results)


    def create_graphs(self, path, lims):
        super().create_graphs(path, lims)

    def create_graphs_for_eeg(self, path, lims):
        super().create_graphs_for_eeg(path, lims)

        aux_df = self._df[["input_type", "input_state", "event_datetime"]]

        fig, axs = plt.subplots(len(aux_df["input_type"].drop_duplicates()), 1, figsize=(14, 6), layout='tight', sharex=True)

        axis_index = 0
        for event in aux_df["input_type"].drop_duplicates().sort_values():
            aux_df[(aux_df["input_type"] == event) & (aux_df["input_state"] == "Started")].plot.scatter(x='event_datetime', y="input_type", c="blue", ax=axs[axis_index])
            aux_df[(aux_df["input_type"] == event) & (aux_df["input_state"] == "Completed")].plot.scatter(x='event_datetime', y="input_type", c="red", ax= axs[axis_index])
            
            axs[axis_index].set_xlim(left=lims[0], right=lims[1])
            axs[axis_index].set_ylabel("")

            axis_index += 1

        plt.xlabel("Time")

        plt.savefig("{0}user_input_eeg".format(path))

#endregion
    
#region METODOS PRIVADOS
       
    def clean_initial_dataframe(self):
        super().clean_initial_dataframe()
        
        self._df = self._df[self._df["scenario_type"] != "MainMenu"]
        self._df = self._df[self._df["scenario_type"] != "LoadingScreen"]
        self._df = self._df[self._df["scenario_type"] != "PlayerScore"]

#enregion