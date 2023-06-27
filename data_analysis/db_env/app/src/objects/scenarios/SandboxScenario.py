from objects.scenarios.Scenario import Scenario

class SandboxScenario(Scenario):

    def __init__(self, user_id: int, experiment_id: int) -> None:
        self.scenario_type = "Sandbox"

        super().__init__(user_id, experiment_id)