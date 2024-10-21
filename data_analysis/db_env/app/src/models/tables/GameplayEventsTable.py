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

    def read_data_from_csv(self) -> None:
        super().read_data_from_csv()
        self._df["event_datetime"] = pd.to_datetime(self._df["event_datetime"], format="%Y-%m-%d %H:%M:%S.%f")

    # read_data_from_csv


    def analyse_data(self) -> None:
        super().analyse_data()
    
    # analyse_data

    def analyse_df(self, df) -> dict:
        super().analyse_df(df)

        start_event = df[df["event_type"] == "00001"].iloc[0]
        end_event = df[df["event_type"] == "00002"].iloc[-1]

        start_time = start_event["event_datetime"]
        end_time = end_event["event_datetime"]

        df = df[((df["event_type"] != "00001") & (df["event_type"] != "00002"))]

        return {
            "TD": round(end_time.timestamp() - start_time.timestamp(), 2),
            "GP_NUM": float(len(df[df["event_state"] == "Completed"])),
            "GP_TIME": self.get_time_btw_datetimes(df[df["event_state"] == "Completed"]["event_datetime"].to_list()),
            "GP_TIME_STARTED_TO_COMPLETED": self.get_time_to_complete_steps(df)
        }
        
    def create_graphs(self):
        pass

    #endregion
        
    #region METODOS PRIVADOS    

    def get_time_to_complete_steps(self, df) -> list:
        
        times_to_complete = []

        completed_df = df[df["event_state"] == "Completed"]
        for row in completed_df.iterrows():
            aux_row = row[1]
            started_df = df[(df["event_state"] == "Started") & (df["event_type"] == aux_row["event_type"])]
            if len(started_df):
                start = started_df.iloc[0]["event_datetime"].timestamp()
                end = aux_row["event_datetime"].timestamp()

                times_to_complete.append(end - start)

        return round(statistics.mean(times_to_complete), 2)
    
    # get_time_to_complete_steps

    #endregion
        


    