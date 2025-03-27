from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, responses
# 📌 Importa `APIRouter` para definir rutas, `Depends` para inyección de dependencias,
# `HTTPException` para manejar errores HTTP, `status` para códigos de estado,
# `Response` para manipular respuestas HTTP y `Cookie` para leer cookies.

from fastapi.security import OAuth2PasswordRequestForm
# 📌 Importa `OAuth2PasswordRequestForm`, que maneja la autenticación basada en OAuth2 con username y password.

from datetime import timedelta
# 📌 Importa `timedelta` para manejar la expiración de los tokens de autenticación.

from sqlalchemy.orm import Session
# 📌 Importa `Session` para interactuar con la base de datos mediante SQLAlchemy.

from jose import JWTError, jwt
# 📌 Importa `JWTError` para manejar errores de tokens y `jwt` para codificar y decodificar JWTs.

from app.api.services import auth_service
# 📌 Importa el servicio de autenticación donde están las funciones para verificar credenciales y generar tokens.

from app.core import settings, get_db
# 📌 Importa `settings`, que contiene la configuración de la aplicación, como claves secretas y tiempos de expiración.
# 📌 Importa `get_db`, que proporciona una sesión de base de datos por solicitud.

from app.api.schemas.auth_schema import Token
# 📌 Importa el esquema `Token`, que define la estructura de la respuesta de autenticación.

# 📌 Se define un enrutador para las rutas de autenticación.
AUTH_ROUTER = APIRouter()

# 🟢 Endpoint para iniciar sesión y generar tokens de acceso y refresco.
@AUTH_ROUTER.post("/auth/login", response_model=Token)
async def login(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Autentica al usuario con sus credenciales y genera un token de acceso y un token de refresco.
    
    - **response**: Objeto de respuesta para manipular cookies.
    - **form_data**: Datos del formulario de autenticación (username y password).
    - **db**: Sesión de base de datos inyectada.
    
    Retorna un diccionario con:
    - `access_token`: Token de acceso válido por un tiempo determinado.
    - `token_type`: Tipo de token (bearer).
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ⏳ Define tiempos de expiración de tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # 🔑 Genera los tokens
    access_token = auth_service.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    # 🍪 Guarda el refresh token en una cookie HTTP-only (segura)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  # 7 días
    )   

    return {"access_token": access_token, "token_type": "bearer", "user": user.id}

# 🟢 Endpoint para refrescar el token de acceso.
@AUTH_ROUTER.post("/auth/refresh")
async def refresh_token(refresh_token: str = Cookie(None)):
    """
    Renueva el token de acceso utilizando el refresh token almacenado en una cookie.

    - **refresh_token**: Token de refresco obtenido de la cookie HTTP-only.

    Retorna un nuevo `access_token` válido.
    """
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token found")

    try:
        # 🔍 Decodifica el refresh token
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # 🔑 Genera un nuevo access token
        new_access_token = auth_service.create_access_token(data={"sub": username})

        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


# 🟢 Endpoint: Cerrar sesión (eliminar cookie de refresh token) #* endpoint agragado 
@AUTH_ROUTER.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Sesión cerrada correctamente"}




""" from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.api.services.auth_service import authenticate_user, create_access_token
from app.core import settings

AUTH_ROUTER = APIRouter()

@AUTH_ROUTER.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"} """








# ! modeloe origianl 
""" from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core import settings
from typing import Dict , Optional


# 🔹 Definición del router
AUTH_ROUTER = APIRouter()

# 🔹 Esquema OAuth2
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/login")

# 🔹 Configuración del contexto de cifrado para contraseñas
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔹 Modelo de usuario simulado
class ModelUser(BaseModel):
    username : str 
    email : str
    full_name : str
    hashed_password : str
    disabled : bool
    

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

# 🔹 Función para verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

# 🔹 Función para obtener un usuario por username
def get_user(username: str) -> Optional[ModelUser]:
    return fake_users_db.get(username)

# 🔹 Función para autenticar un usuario
def authenticate_user(username: str, password: str) -> Optional[ModelUser]:
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# 🔹 Función para crear un token JWT
def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# 🔹 Endpoint para login
@AUTH_ROUTER.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"} """



""" @AUTH_ROUTER.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"username": form_data.username, "password": form_data.password} """


""" 
# backend/app/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.auth import authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter()

# Endpoint de login que devuelve el token JWT
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
"""