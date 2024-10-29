from enums.E_UserInputType import UserInputType

from models.tables.events.Table import *

class UserInputEventsTable(Table):
    '''
    Class UserInputEventsTable
    -------------------

    La clase UserInputEventsTable ...
    '''
#region VARIABLES GLOBALES
    
    
#endregion
    
#region METODOS PUBLICOS

    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="user_input")


    def set_data(self) -> None:
        super().set_data()

    def read_data(self) -> None:
        super().read_data()
        self._df = self._df.reset_index()
        
        for index, row in self._df.iterrows():
            self._df.at[index, "input_type"] = '_'.join(self._df.at[index, "input_type"].split("_")[:-1])
        
        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        
    def analyse_data(self):
        super().analyse_data()

    def analyse_df(self, df) -> dict:
        return super().analyse_df(df)
        
    def analyse_number(self, df):
        results = {}

        # Número de inputs totales
        results["UI_N"] = float(len(df))
        # Número de inputs con la mano derecha
        results["UI_N_R"] = float(len(df[df["hand"] == "Right"]))
        # Número de inputs con la mano izquierda
        results["UI_N_L"] = float(len(df[df["hand"] == "Left"]))

        # Número de inputs de cada tipo
        for index in UserInputType:
            results["UI_N_t_{0}".format(index.value)] = float(len(df[df["input_type"].str.upper() == index.name]))
            # Número de inputs con la mano derecha
            results["UI_N_t_{0}_R".format(index.value)] = float(len(df[(df["input_type"].str.upper() == index.name) & (df["hand"] == "Right")]))
            # Número de inputs con la mano izquierda
            results["UI_N_t_{0}_L".format(index.value)] = float(len(df[(df["input_type"].str.upper() == index.name) & (df["hand"] == "Left")]))

        return results

    
    def analyse_time(self, df):
        results = {}

        results["UI_T"] = self.get_time_btw_datetimes(df["event_datetime"].to_list())

        # Tiempo desde que se inicia (STARTED) hasta que se completa (COMPLETED) el evento generico
        right = self.get_time_btw_two_type(
                df[(df["hand"] == "Right") & (df["input_state"] == "started")],
                df[(df["hand"] == "Right") & (df["input_state"] == "completed")], ["scenario_type"])
        left = self.get_time_btw_two_type(
                df[(df["hand"] == "Left") & (df["input_state"] == "started")],
                df[(df["hand"] == "Left") & (df["input_state"] == "completed")], ["scenario_type"])
    
        results["UI_T_SC"] = round(np.nanmean([right, left]), 3)
        
        # Tiempo desde que se inicia (STARTED) hasta que se completa (COMPLETED) el evento especifico
        for index in UserInputType:
            results["UI_T_SC_t_{0}".format(index.value)] = 0.0

            right = self.get_time_btw_two_type(
                    df[(df["hand"] == "Right") & (df["input_type"].str.upper() == index.name) & (df["input_state"] == "started")],
                    df[(df["hand"] == "Right") & (df["input_type"].str.upper() == index.name) & (df["input_state"] == "completed")], ["scenario_type"])
            left = self.get_time_btw_two_type(
                    df[(df["hand"] == "Left") & (df["input_type"].str.upper() == index.name) & (df["input_state"] == "started")],
                    df[(df["hand"] == "Left") & (df["input_type"].str.upper() == index.name) & (df["input_state"] == "completed")], ["scenario_type"])
    
            results["UI_T_SC_t_{0}".format(index.value)] = round(np.nanmean([right, left]), 3)
        return results


    def create_graphs(self):
        pass

#endregion
    
#region METODOS PRIVADOS
       
#enregion