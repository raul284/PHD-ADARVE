from objects.scenarios.Scenary import Scenary

class CarAccidentScenary(Scenary):

    def __init__(self, db, user_ids: list) -> None:
        super().__init__(db, user_ids)