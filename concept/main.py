from decorator.provides import Provides
from dao import CarDao, EngineDao
from core import Provider

class Module(Provider):
    @Provides
    def get_engine_dao(self) -> EngineDao:
        return EngineDao()
    
    @Provides
    def get_car_dao(self, engine_dao: EngineDao) -> CarDao:
        return CarDao(engine = engine_dao)

if __name__ == "__main__":    
    app = Module()
    carDao = app.get(CarDao)
    print(carDao)

