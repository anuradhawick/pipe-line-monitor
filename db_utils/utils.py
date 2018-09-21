import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

session = None

def get_engine():
    return create_engine(
        'sqlite:///' + os.getcwd() + '/db/database.db', echo=False)


def get_session():
    global session

    if(session):
        return session

    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    return session
