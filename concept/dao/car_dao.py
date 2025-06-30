from dao.engine_dao import EngineDao

class CarDao:
    """Data Access Object (DAO) for persistent car entity operations.

    Attributes:
        engine (Engine): Engine component used for powering persistence operations.
    """
    engine: EngineDao

    def __init__(self, engine: EngineDao) -> None:
        """Initializes the Car DAO with required dependencies.

        Args:
            engine: Valid Engine instance that meets persistence requirements.

        """
        self.engine = engine