from __future__ import annotations
from sqlalchemy import Column, String, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

# 🚀 Tabla de Predicciones
class Prediction(Base):
    """
    Modelo de base de datos para almacenar predicciones realizadas por los usuarios.

    Atributos:
        id (UUID): Identificador único de la predicción.
        user_id (UUID): Referencia al usuario que realizó la predicción.
        brand (str): Marca del vehículo.
        model (str): Modelo del vehículo.
        year (int): Año del vehículo.
        engine_size (float): Tamaño del motor en litros.
        fuel_type (str): Tipo de combustible del vehículo.
        transmission (str): Tipo de transmisión del vehículo.
        mileage (int): Kilometraje del vehículo.
        doors (int): Número de puertas del vehículo.
        owner_count (int): Número de dueños previos del vehículo.
        created_at (TIMESTAMP): Fecha de creación de la predicción.
        
        user (relationship): Relación con el usuario propietario de la predicción.
        model1_result (relationship): Relación con la tabla PricesCluster (modelo 1: KMeans y DBSCAN).
        model2_result (relationship): Relación con la tabla PricesSegmentation (modelo 2: RF, SVM, MLP).
        model3_result (relationship): Relación con la tabla PricesPrediction (modelo 3: modelo de predicción de precios).
    """

    __tablename__ = "predictions"

    # Identificador único de la predicción
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    
    # Relación con el usuario que realizó la predicción
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Datos del vehículo
    brand = Column(String(100), nullable=False)  # Marca del auto
    model = Column(String(100), nullable=False)  # Modelo del auto
    year = Column(Integer, nullable=False)  # Año del auto
    engine_size = Column(Float, nullable=False)  # Tamaño del motor en litros
    fuel_type = Column(String(50), nullable=False)  # Tipo de combustible
    transmission = Column(String(50), nullable=False)  # Tipo de transmisión
    mileage = Column(Integer, nullable=False)  # Kilometraje del vehículo
    doors = Column(Integer, nullable=False)  # Número de puertas
    owner_count = Column(Integer, nullable=False)  # Número de dueños previos

    # Fecha de creación de la predicción
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relación con el usuario que realizó la predicción
    user = relationship("User", back_populates="predictions")

    # Relación con los resultados de los modelos de predicción
    model1_result = relationship("PricesCluster", back_populates="prediction", uselist=False)  # Modelo 1: KMeans y DBSCAN
    model2_result = relationship("PricesSegmentation", back_populates="prediction", uselist=False)  # Modelo 2: RF, SVM, MLP
    model3_result = relationship("PricesPrediction", back_populates="prediction", uselist=False)  # Modelo 3: Predicción de precios
