from objects.events.Events import Events

class InteractEvents(Events):

    def __init__(self, raw_data) -> None:
        super().__init__(raw_data)

    def get_results(self):
        return super().get_results()

    def get_results_for_global_analysis(self) -> dict:
        aux_dict = super().get_results_for_global_analysis()
        return aux_dict