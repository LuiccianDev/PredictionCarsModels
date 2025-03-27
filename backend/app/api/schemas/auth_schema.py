from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID

# 📌 Esquema base de usuario
# Este esquema define los atributos comunes que tendrá cualquier usuario en el sistema.
class UserBase(BaseModel):
    username: str  # Nombre de usuario (obligatorio)
    email: EmailStr  # Correo electrónico validado (obligatorio)

# 📌 Esquema para la creación de usuario
# Hereda de UserBase e incluye la contraseña, que es necesaria al registrar un usuario.
class UserCreate(UserBase):
    password: str  # Contraseña del usuario (obligatorio)

# 📌 Esquema para representar a un usuario en la respuesta de la API
# Incluye una bandera `disabled` que indica si la cuenta está deshabilitada o no.
class User(UserBase):
    disabled: Optional[bool] = None  # Indica si la cuenta del usuario está deshabilitada (opcional)

    # Configuración del modelo en Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# 📌 Esquema para manejar los tokens de autenticación
# Se usa para devolver el token de acceso después de que un usuario inicia sesión correctamente.
class Token(BaseModel):
    access_token: str  # Token de acceso generado (JWT u otro formato)
    token_type: str  # Tipo de token (normalmente "bearer")
    user : UUID  #! cambio

# 📌 Esquema para manejar los datos del token
# Se utiliza para extraer información del token, como el nombre de usuario autenticado.
class TokenData(BaseModel):
    username: Optional[str] = None  # Nombre de usuario extraído del token (opcional)


""" class ModelUser(BaseModel):
    username: str = Field(..., example="johndoe") # field()
    email: str = Field(..., example="johndoe@example.com")
    hashed_password: str 
    disabled: bool """