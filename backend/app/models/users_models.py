from __future__ import annotations  
# Permite el uso de anotaciones de tipo futuras en Python, útil para evitar problemas con las relaciones de SQLAlchemy.

from sqlalchemy import Column, String, TIMESTAMP  
# Importa los tipos de columnas necesarias para definir la estructura de la tabla en la base de datos.

from sqlalchemy.dialects.postgresql import UUID  
# Permite el uso del tipo de dato UUID específico para PostgreSQL.

from app.core.database import Base  
# Importa la clase `Base`, que sirve como base para definir los modelos de SQLAlchemy.

import uuid  
# Proporciona la funcionalidad para generar identificadores únicos (UUID) automáticamente.

from sqlalchemy.orm import relationship  
# Permite definir relaciones entre modelos dentro de SQLAlchemy.

from sqlalchemy.sql import func  
# Proporciona funciones SQL, como `func.now()` para generar timestamps automáticos.

# 🚀 Tabla de Usuarios
class User(Base):
    """
    Modelo de base de datos que representa la tabla `users`.

    Atributos:
        id (UUID): Identificador único del usuario.
        email (str): Dirección de correo electrónico del usuario (única).
        username (str): Nombre de usuario (único).
        hashed_password (str): Contraseña del usuario almacenada en formato encriptado.
        created_at (TIMESTAMP): Fecha y hora de creación del usuario.
        predictions (relationship): Relación con la tabla `Prediction`, para acceder a las predicciones realizadas por el usuario.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)  # Email único del usuario
    username = Column(String(100), unique=True, nullable=False)  # Nombre de usuario único
    hashed_password = Column(String(255), nullable=False)  # Contraseña almacenada en formato hash
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())  # Fecha de creación del usuario

    # Relación con la tabla `Prediction`
    predictions = relationship("Prediction", back_populates="user")

