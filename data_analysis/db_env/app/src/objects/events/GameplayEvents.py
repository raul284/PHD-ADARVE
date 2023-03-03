from objects.events.Events import Events

GAMEPLAY_TYPES = ["CA_Start", "CA_TalkToWorker", "CA_ProtectDriver", "CA_TalkToDriver", \
    "CA_StopTraffic", "CA_InspectVan", "CA_MeasureRadiation", "CA_ReportToOffice", "CA_Finish"]

class GameplayEvents(Events):

    # Informacion sobre si se han completado todos los eventos del gameplay
    complete_all_steps: bool
    # Lista con el conteo de las repeticiones de cada uno de los eventos
    steps_repetition: dict

    # Si los eventos se han realizado en orden
    in_order: bool
    # El orden en el que se han realizado los eventos
    steps_order: dict


    def __init__(self, raw_data) -> None:
        super().__init__(raw_data)

        self.is_completed()
        self.is_in_order()


    def is_completed(self):
        duplicate_removed = []
        aux_events = [event["event_type"] for event in self.events]
        [duplicate_removed.append(event) for event in aux_events if event not in duplicate_removed]

        self.complete_all_steps = len(duplicate_removed) == len(GAMEPLAY_TYPES)
        self.steps_repetition = {event : aux_events.count(event) for event in GAMEPLAY_TYPES}

    def is_in_order(self):
        duplicate_removed = []
        aux_events = [event["event_type"] for event in self.events]
        [duplicate_removed.append(event) for event in aux_events if event not in duplicate_removed]
        
        order = {}
        for event in GAMEPLAY_TYPES:
            if event in duplicate_removed:
                order[event] = duplicate_removed.index(event)
            else:
                order[event] = -1

        self.in_order = duplicate_removed == GAMEPLAY_TYPES
        self.steps_order = order

    def get_results(self):
        results = super().get_results()
        results["completed"] = {
            "allSteps": self.complete_all_steps,
            "repeatedSteps": self.steps_repetition
        }
        results["order"] = {
            "inOrder": self.in_order,
            "stepsOrder": self.steps_order
        }

        return results

    def get_results_for_global_analysis(self) -> dict:
        aux_dict = super().get_results_for_global_analysis()
        return aux_dict