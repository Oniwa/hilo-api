import sqlalchemy
import sqlalchemy.orm
import db.db_folder as db_folder
from models.model_base import ModelBase
# TODO: add all models to be imported here
# noinspection PyUnresolvedReferences
from models import move, player

__factory = None


def global_init():
    global __factory

    full_file = db_folder.get_db_folder('hilo.sqlite')
    conn_str = 'sqlite:///'

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    ModelBase.metadata.create_all(engine)

    __factory = sqlalchemy.orm.sessionmaker(bind=engine)


def create_session():
    global __factory

    if __factory is None:
        global_init()

    return __factory()