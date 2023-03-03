from database.models import InteractEventDB, GameplayEventDB, MoveEventDB
from objects.phases.Phase import Phase
from objects.phases.LaboratoryPhase import LaboratoryPhase
from objects.scenarios.Scenary import Scenary


class LaboratoryScenary(Scenary):

    def __init__(self, db, user_ids: list) -> None:
        super().__init__(db, user_ids)

    def set_phase(self, id: int) -> Phase:
        '''
        Crea un objeto de tipo Phase, y lo devuelve, con los datos las interacciones que ha realizado el usuario con el
        identificador indicado.

        :param id: Identificado del usuario en la base de datos
        :return: Devuelve un objeto de tipo Phase
        '''

        # Crea el objeto de tipo clase
        phase = LaboratoryPhase()

        # Asigna los datos de la fase. Para ello coge la informacion de la base de datos en base al indentificador.
        # La informacion se divide en N listas siendo N el numero de tipos de interacciones distintas. La lista que
        # proporciona la base de datos se ordena segun el instante de tiempo que se realizo dicho evento.
        #
        phase.set_data(
            # Lista de los objetivos del gameplay
            sorted(
                [event.as_dict() for event in self.db.query(GameplayEventDB).filter(GameplayEventDB.user_id == id).all()], 
                key=lambda d: d["event_datetime"]),
            # Lista de las interacciones realizadas con los objetos
            sorted(
                [event.as_dict() for event in self.db.query(InteractEventDB).filter(InteractEventDB.user_id == id).all()], 
                key=lambda d: d["event_datetime"]),
            # Lista de los movimientos que realizan los usuarios
            sorted(
                [event.as_dict() for event in self.db.query(MoveEventDB).filter(MoveEventDB.user_id == id).all()],
                key=lambda d: d["start_datetime"])
        )

        # Devuelve la fase
        return phase

    # set_phases