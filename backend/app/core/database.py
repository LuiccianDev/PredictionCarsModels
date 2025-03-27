from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Creación de la conexión a la base de datos
engine = create_engine(settings.DATABASE_URL)  # Se crea el motor de base de datos con la URL definida en settings

# Creación de la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaración de la base para los modelos de SQLAlchemy
Base = declarative_base()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    
    Importa los modelos antes de la creación de tablas para asegurarse de que SQLAlchemy los registre.
    """
    from app.models import users_models, predictions_models, result_prediction_models
    Base.metadata.create_all(bind=engine)  # Crea las tablas en la base de datos si no existen

def get_db():
    """
    Proporciona una sesión de base de datos para ser usada en las operaciones CRUD.
    
    Yields:
        db (Session): Sesión de SQLAlchemy para interactuar con la base de datos.
    
    Asegura que la sesión se cierre después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
