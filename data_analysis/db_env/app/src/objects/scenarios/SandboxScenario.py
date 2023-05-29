from objects.scenarios.Scenario import Scenario

class SandboxScenario(Scenario):

    def __init__(self, db, user_id: int) -> None:
        self.scenario_type = "Sandbox"

        super().__init__(db, user_id)