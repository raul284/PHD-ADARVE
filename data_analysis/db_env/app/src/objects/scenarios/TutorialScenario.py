from objects.scenarios.Scenario import Scenario

class TutorialScenario(Scenario):

    def __init__(self, user_id: int, experiment_id: int) -> None:
        self.scenario_type = "Tutorial"

        super().__init__(user_id, experiment_id)