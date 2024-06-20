from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models import Base

def memory_engine():
    """
        Créer un engine sqlalchemy qui utilise la mémoire
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    database = scoped_session(session_factory)

    return database
