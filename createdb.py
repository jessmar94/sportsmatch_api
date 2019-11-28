from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def createdb(database_url):
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)

    print(database_exists(engine.url))
