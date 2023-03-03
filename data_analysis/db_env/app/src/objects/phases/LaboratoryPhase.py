from objects.phases.Phase import Phase

class LaboratoryPhase(Phase):

    measured_correct: int
    measured_incorrect: int

    def __init__(self) -> None:
        super().__init__()

    def set_data(self, gameplay_events, interact_events, move_events) -> None:
        super().set_data(gameplay_events, interact_events, move_events)

        self.set_measured_radiation_info()


    def set_measured_radiation_info(self) -> None:
        self.measured_correct = 0
        self.measured_incorrect = 0

        for event in self.data["interact"].events:
            if event.event_type == "measured_correct":
                self.measured_correct += 1
            elif event.event_type == "measured_incorrect":
                self.measured_incorrect += 1

    # set_measured_radiation_info


    def analyse_data(self) -> None:
        super().analyse_data()

        self.results["measures"] = round(self.measured_correct / (self.measured_correct + self.measured_incorrect), 2)

    # analyse_data


    def get_results_for_global_analysis(self) -> dict:
        aux_dict = super().get_results_for_global_analysis()

        aux_dict["measures"] = self.results["measures"]

        return aux_dict
    
    # get_results_for_global_analysis

