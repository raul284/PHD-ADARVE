import statistics

from models.tables.Table import *


class GameplayEventsTable(Table):
    '''
    Class GameplayEventsTable
    ------------------------------

    Datos de entrada:
    - id
    - user_id
    - scenario_type
    - event_state: Estado del evento de gameplay [Started, Completed]
    - event_type: Tipo de evento
    - event_datetime: Fecha y hora en la que se ha realizado el evento

    Resultados:
    - total_duration: Duracion total desde el evento Start hasta el evento Finish
    - num_of_started: Cantidad de eventos de gameplay iniciados
    - num_of_completed: Cantidad de eventos de gameplay terminados
    - time_btw_steps: Tiempo medio entre los eventos de gameplay terminados

    '''

    #region VARIABLES PUBLICAS


    #endregion
    
    #region METODOS PUBLICOS

    def __init__(self, user_data) -> None:

        super().__init__(user_data=user_data, table_name="gameplay")

    # __init__

    def set_data(self) -> None:
        super().set_data()

    def read_data(self) -> None:
        super().read_data()

        # Para aquellos escenarios donde no haya evento de STARTED los creo a partir del evento de COMPLETED anterior.Por ejemplo en el S2
        # eventos STARTED. Lo que hago es para S2002 creo el evento STARTED con el datetime del COMPLETED de S2001.
        df = self._df[self._df["scenario_type"] == "S2"].assign(event_state = "Started")
        for i in range(0, len(df) - 1):
            df.at[i, "event_type"] = df.at[i + 1, "event_type"]
        
        self._df = pd.concat([self._df, df[:-2]], ignore_index=True)

        self._df["event_datetime"] = pd.to_datetime(self.fix_datetimes(self._df["event_datetime"]), format="%Y-%m-%d %H:%M:%S.%f")
        self._df = self._df.sort_values(by=["event_datetime", "event_type"])

    # read_data_from_csv


    def analyse_data(self) -> None:
        super().analyse_data()
    
    # analyse_data

    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        self._start_event = df[df["event_type"] == "00001"].iloc[0]
        self._end_event = df[df["event_type"] == "00002"].iloc[-1]

        start_time = self._start_event["event_datetime"]
        end_time = self._end_event["event_datetime"]

        df = df[((df["event_type"] != "00001") & (df["event_type"] != "00002"))]

        return {
            "TD": round(end_time.timestamp() - start_time.timestamp(), 2),
            "GP_N": float(len(df[df["event_state"] == "Completed"])),
            "GP_T": self.get_time_btw_datetimes(df[df["event_state"] == "Completed"]["event_datetime"].to_list()),
            "GP_T_SC": self.get_time_btw_two_type(df[df["event_state"] == "Started"], df[df["event_state"] == "Completed"])
        }
        
    def create_graphs(self):
        pass

    #endregion
        
    #region METODOS PRIVADOS    

    def get_time_to_complete_steps(self, df) -> list:
        
        times_to_complete = []

        print(df)

        completed_df = df[df["event_state"] == "Completed"]
        for row in completed_df.iterrows():
            aux_row = row[1]
            started_df = df[(df["event_state"] == "Started") & (df["event_type"] == aux_row["event_type"])]
            if started_df.empty:
                print("hola")
            else: 
                print(started_df)
            if len(started_df):
                start = started_df.iloc[0]["event_datetime"].timestamp()
                end = aux_row["event_datetime"].timestamp()

                times_to_complete.append(end - start)

        if len(times_to_complete) > 0: return round(statistics.mean(times_to_complete), 3)
        else: np.nan
    
    # get_time_to_complete_steps

    def get_time_btw_two_type(self, fst_df, snd_df):
        super().get_time_btw_two_type(fst_df, snd_df)

        time_btw = []

        print(snd_df)

        while not fst_df.empty and not snd_df.empty:
            first_event = fst_df.iloc[0]
            snd_event = snd_df[(snd_df["event_type"] == first_event["event_type"])].iloc[0]
            
            time = self.get_time_btw_datetimes([first_event["event_datetime"], snd_event["event_datetime"]])
            if time < 0: print("Hay un tiempo entre interacciones negativo.")

            time_btw.append(time)

            fst_df = fst_df.iloc[1:]
            snd_df = snd_df.drop(snd_df[
                (snd_df["event_type"] == first_event["event_type"])].index[0])

        if len(time_btw) > 0: return statistics.mean(time_btw)
        else: return np.nan

    #endregion
        


    