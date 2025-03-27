# 📌 Importaciones necesarias
from pydantic import BaseModel, EmailStr, Field  # Validación de datos
from typing import Optional  # Permite campos opcionales
from uuid import UUID  # Manejo de identificadores únicos

"""  Importaciones
        BaseModel → Define la estructura de los esquemas.
        EmailStr → Valida que el campo email tenga formato de correo electrónico.
        Field → Permite agregar restricciones y ejemplos a los campos.
        Optional → Indica que un campo puede ser opcional.
        UUID → Se usa para asignar identificadores únicos a los usuarios. """

# 📌 Esquema base de usuario
class UserBase(BaseModel):
    """
    Esquema base que define los atributos comunes de un usuario.

    Atributos:
        username (str): Nombre de usuario (obligatorio).
        email (EmailStr): Dirección de correo electrónico válida (obligatorio).
    """
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")


# 📌 Esquema para la creación de un usuario
class UserCreate(UserBase):
    """
    Esquema para la creación de un nuevo usuario.

    Hereda de:
        UserBase (incluye username y email).

    Atributos adicionales:
        password (str): Contraseña del usuario (mínimo 6 caracteres, obligatorio).
    """
    password: str = Field(..., min_length=6, example="secret123")


# 📌 Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    """
    Esquema para la actualización de datos de un usuario.

    Atributos:
        username (Optional[str]): Nuevo nombre de usuario (opcional).
        email (Optional[EmailStr]): Nueva dirección de correo electrónico válida (opcional).
    """
    username: Optional[str] = Field(None, example="johndoe_updated")
    email: Optional[EmailStr] = Field(None, example="johndoe_updated@example.com")


# 📌 Esquema de respuesta del usuario (sin contraseña)
class UserResponse(UserBase):
    """
    Esquema para la respuesta de usuario en la API.

    Hereda de:
        UserBase (incluye username y email).

    Atributos adicionales:
        id (UUID): Identificador único del usuario en la base de datos.
    
    **Nota:** No se incluye la contraseña por razones de seguridad.
    """
    id: UUID
