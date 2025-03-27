import os
from pydantic_settings import BaseSettings
import yaml
from dotenv import load_dotenv
from typing import Dict

# Cargar variables de entorno desde el archivo .env
DOTENV_PATH = os.path.join(os.path.dirname(__file__), ".env")  # Ruta al archivo .env
YAML_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")  # Ruta al archivo config.yaml
load_dotenv(DOTENV_PATH)  # Carga las variables de entorno desde el archivo .env

# Cargar configuración desde el archivo YAML antes de definir la clase Settings
with open(YAML_PATH, mode="r", encoding="utf-8") as fs:
    CONFIG_YAML = yaml.safe_load(fs)  # Lee y parsea el archivo YAML

class Settings(BaseSettings):
    """
    Clase que gestiona la configuración de la aplicación.
    
    Carga variables desde los archivos .env y config.yaml para ser utilizadas en la aplicación.
    """

    # Variables cargadas desde el archivo .env
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")  # Usuario de la base de datos
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")  # Contraseña de la base de datos
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")  # Nombre de la base de datos
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")  # Host de la base de datos
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))  # Puerto de la base de datos (por defecto 5432)
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # Clave secreta para autenticación

    # Variables cargadas desde config.yaml (seguridad)
    ALGORITHM: str = CONFIG_YAML["security"]["algorithm"]  # Algoritmo de cifrado
    ACCESS_TOKEN_EXPIRE_MINUTES: int = CONFIG_YAML["security"]["access_token_expire_minutes"]  # Tiempo de expiración del token de acceso
    REFRESH_TOKEN_EXPIRE_DAYS: int = CONFIG_YAML["security"]["refresh_token_expire_days"]  # Tiempo de expiración del token de actualización

    # Configuración de modelos de predicción desde config.yaml
    MODELS_NAME_PREDICT: Dict[str, str] = CONFIG_YAML["models_name_predict"]  # Nombres de los modelos de predicción
    MODELS_PATH: Dict[str, str] = CONFIG_YAML["models_path"]  # Rutas de los modelos de predicción

    # Endpoints de la aplicación desde config.yaml
    PREDICTIONS: Dict[str, str] = CONFIG_YAML["endpoints"]["predictions"]  # Endpoints de predicciones
    AUTH: Dict[str, str] = CONFIG_YAML["endpoints"]["auth"]  # Endpoints de autenticación
    USERS: Dict[str, str] = CONFIG_YAML["endpoints"]["users"]  # Endpoints de usuarios

    # Construcción de la URL de conexión a la base de datos
    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

# Crear una instancia de Settings para su uso en la aplicación
settings = Settings()



