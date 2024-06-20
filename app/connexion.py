import os
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models import Base as BaseModel

load_dotenv()

database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')
unix_socket_path  = os.getenv('INSTANCE_UNIX_SOCKET')
environment_mode = os.getenv('ENVIRONMENT_MODE')
database_host = os.getenv("DATABASE_HOST")

def engine_dev():
    """
        Connexion à la base de donnée dev
    """
    database_url = f"mysql+pymysql://{database_username}:" \
        f"{database_password}@{database_host}/paye-ton-kawa-Commande"
    return sqlalchemy.create_engine(database_url, echo=True)

def engine_cloud():
    """
        Connexion à la base de données cloud sql
    """
    return sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username=database_username,
                password=database_password,
                database="paye-ton-kawa",
                host="",
                port=None,
                query={
                "unix_socket": unix_socket_path
            }
        )
    )

engine = engine_dev() if environment_mode == "dev" else engine_cloud()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    """
        Créer et retourne une instance la connexion à la base de donnée
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
        Test la connexion.
        Provoque une exception si l'api n'arrive pas à se connecter à la base de données
        Créer les tables si réussie
    """
    BaseModel.metadata.create_all(engine)
