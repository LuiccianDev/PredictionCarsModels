from sqlalchemy.orm import Session
from uuid import uuid4
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.api.schemas.users_schema import UserCreate, UserUpdate, UserResponse
from app.models import User

# Contexto para el hash de contraseñas con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_service(user: UserCreate, db: Session) -> UserResponse:
    """
    Crea un nuevo usuario en la base de datos.
    
    :param user: Objeto de entrada con los datos del usuario.
    :param db: Sesión de la base de datos.
    :return: Objeto UserResponse con los datos del usuario creado.
    """
    user_id = str(uuid4())  # Genera un ID único para el usuario
    hashed_password = pwd_context.hash(user.password)  # Hashea la contraseña
    
    # Creación del objeto de usuario para la BD
    db_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)  # Agregar usuario a la sesión de la BD
    db.commit()  # Guardar cambios en la BD
    db.refresh(db_user)  # Refrescar para obtener datos actualizados
    
    return UserResponse(id=user_id, username=user.username, email=user.email)


def get_user_service(user_id: str, db: Session) -> UserResponse:
    """
    Obtiene un usuario por su ID desde la base de datos.
    
    :param user_id: ID del usuario a buscar.
    :param db: Sesión de la base de datos.
    :return: Objeto UserResponse con los datos del usuario.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserResponse(id=user.id, username=user.username, email=user.email)


def update_user_service(user_id: str, user_update: UserUpdate, db: Session) -> UserResponse:
    """
    Actualiza los datos de un usuario en la base de datos.
    
    :param user_id: ID del usuario a actualizar.
    :param user_update: Objeto con los campos a actualizar.
    :param db: Sesión de la base de datos.
    :return: Objeto UserResponse con los datos actualizados del usuario.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Actualización de los campos proporcionados
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    
    db.commit()  # Guardar cambios en la BD
    db.refresh(user)  # Refrescar el usuario con los datos actualizados
    
    return UserResponse(id=user.id, username=user.username, email=user.email)


def delete_user_service(user_id: str, db: Session) -> dict:
    """
    Elimina un usuario de la base de datos.
    
    :param user_id: ID del usuario a eliminar.
    :param db: Sesión de la base de datos.
    :return: Diccionario con mensaje de confirmación.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)  # Eliminar usuario de la BD
    db.commit()  # Confirmar eliminación
    
    return {"message": f"User {user_id} deleted successfully!"}


