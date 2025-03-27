"""
Módulo de autenticación y manejo de tokens JWT en FastAPI.

Este módulo proporciona funciones para:
- Hashing y verificación de contraseñas.
- Autenticación de usuarios en la base de datos.
- Creación de tokens de acceso y refresco para autenticación.

Requisitos:
- `jose` para generar y validar tokens JWT.
- `passlib` para el manejo seguro de contraseñas.
- `sqlalchemy` para la consulta de usuarios en la base de datos.
"""

from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import jwt  # Manejo de JSON Web Tokens
from passlib.context import CryptContext  # Hashing de contraseñas
from sqlalchemy.orm import Session  # Sesión de base de datos con SQLAlchemy

# Importación de esquemas y configuraciones del proyecto
from app.api.schemas.auth_schema import Token, TokenData  # Esquemas de autenticación
from app.core import settings  # Configuración global del proyecto
from app.models import User as UserModel  # Modelo de usuario

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su versión hasheada.
    
    :param plain_password: Contraseña en texto plano ingresada por el usuario.
    :param hashed_password: Contraseña almacenada en la base de datos (hasheada).
    :return: `True` si las contraseñas coinciden, `False` en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, email: str) -> Optional[UserModel]:
    """
    Busca un usuario en la base de datos por su correo electrónico.
    
    :param db: Sesión de base de datos de SQLAlchemy.
    :param email: Correo electrónico del usuario a buscar.
    :return: Objeto `UserModel` si se encuentra el usuario, `None` si no existe.
    """
    return db.query(UserModel).filter(UserModel.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[UserModel]:
    """
    Autentica a un usuario verificando su email y contraseña.
    
    :param db: Sesión de base de datos de SQLAlchemy.
    :param email: Correo electrónico del usuario.
    :param password: Contraseña en texto plano ingresada por el usuario.
    :return: Objeto `UserModel` si la autenticación es exitosa, `None` en caso contrario.
    """
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token de acceso JWT con una expiración definida.
    
    :param data: Datos a incluir en el token (por ejemplo, `sub: user_id`).
    :param expires_delta: Tiempo de expiración del token (por defecto, 15 minutos).
    :return: Token JWT codificado como string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token de refresco JWT con una expiración más larga.
    
    :param data: Datos a incluir en el token (por ejemplo, `sub: user_id`).
    :param expires_delta: Tiempo de expiración del token (por defecto, 7 días).
    :return: Token JWT codificado como string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))  # 7 días
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


""" from typing import Dict, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.api.schemas.auth_schema import ModelUser
from app.core import settings

# 🔹 Configuración de cifrado de contraseñas
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Base de datos de usuarios simulada
fake_users_db: Dict[str, ModelUser] = {
    "usuario1": ModelUser(
        username="usuario1",
        full_name="Usuario Uno",
        email="usuario1@example.com",
        hashed_password=PWD_CONTEXT.hash("secret"),  # Contraseña encriptada
        disabled=False,
    )
}

# 🔹 Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

# 🔹 Función para obtener usuario por username
def get_user(username: str) -> Optional[ModelUser]:
    return fake_users_db.get(username)

# 🔹 Función para autenticar un usuario
def authenticate_user(username: str, password: str) -> Optional[ModelUser]:
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# 🔹 Función para generar un token JWT
def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) """