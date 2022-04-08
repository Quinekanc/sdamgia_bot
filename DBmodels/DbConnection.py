import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from utils.Log import log


SqlAlchemyBase = dec.declarative_base()

__factory = None


def InitDb(dbFilePath: str):
    """
    Инициализировать Базу Данных SQLite
    :param dbFilePath: Путь до SQLite БД
    """

    global __factory
    if __factory:
        return
    if not dbFilePath or not dbFilePath.strip():
        raise Exception("Incorrect db file path")

    connectionStr = f"""sqlite:///{dbFilePath.strip()}?check_same_thread=False"""
    log("Initialising DB")

    engine = sqlalchemy.create_engine(connectionStr, echo=False)
    __factory = sqlalchemy.orm.sessionmaker(bind=engine)

    from . import DbModels

    SqlAlchemyBase.metadata.create_all(engine)


def CreateSession() -> Session:
    global __factory
    return __factory()
