from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.services.user_service import (create_user_service, 
                                           get_user_service, 
                                           update_user_service, 
                                           delete_user_service
)
from app.api.schemas.users_schema import UserCreate, UserUpdate, UserResponse
from app.core import get_db  # Se importa la función para obtener la sesión de la base de datos

# 📌 Creación del enrutador para manejar las rutas relacionadas con usuarios
USER_ROUTER = APIRouter()

# 🔹 Endpoint para registrar un usuario
@USER_ROUTER.post("/users/register", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.

    Parámetros:
    - user (UserCreate): Datos del usuario a registrar.
    - db (Session): Sesión de base de datos proporcionada por FastAPI.

    Retorna:
    - UserResponse: Datos del usuario creado.
    """
    return create_user_service(user, db)

# 🔹 Endpoint para obtener un usuario por ID
@USER_ROUTER.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Obtiene la información de un usuario específico.

    Parámetros:
    - user_id (str): Identificador único del usuario.
    - db (Session): Sesión de base de datos.

    Retorna:
    - UserResponse: Datos del usuario encontrado.
    """
    return get_user_service(user_id, db)

# 🔹 Endpoint para actualizar un usuario
@USER_ROUTER.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de un usuario existente.

    Parámetros:
    - user_id (str): Identificador único del usuario.
    - user_update (UserUpdate): Datos a actualizar.
    - db (Session): Sesión de base de datos.

    Retorna:
    - UserResponse: Datos del usuario actualizado.
    """
    return update_user_service(user_id, user_update, db)

# 🔹 Endpoint para eliminar un usuario
@USER_ROUTER.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos.

    Parámetros:
    - user_id (str): Identificador único del usuario.
    - db (Session): Sesión de base de datos.

    Retorna:
    - dict: Mensaje de confirmación de eliminación.
    """
    return delete_user_service(user_id, db)
