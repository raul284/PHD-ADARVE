from objects.scenarios.Scenario import Scenario

class CarAccidentScenario(Scenario):

    def __init__(self, db, user_id: int) -> None:
        self.scenario_type = "CarAccident"

        super().__init__(db, user_id)