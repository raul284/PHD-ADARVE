from objects.scenarios.Scenario import Scenario

class TutorialScenario(Scenario):

    def __init__(self, db, user_id: int) -> None:
        self.scenario_type = "Tutorial"

        super().__init__(db, user_id)