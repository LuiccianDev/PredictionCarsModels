from __future__ import annotations
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, JSON, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

# 🚀 Tabla de Resultados del Modelo 1 (KMeans y DBSCAN)
class PricesCluster(Base):
    """
    Modelo de base de datos para almacenar los resultados del modelo de clusterización (KMeans y DBSCAN).

    Atributos:
        id (UUID): Identificador único del resultado de clusterización.
        prediction_id (UUID): Referencia a la predicción asociada.
        kmeans_cluster (int): Identificador del clúster asignado por KMeans.
        dbscan_cluster (int): Identificador del clúster asignado por DBSCAN.
        prediction (relationship): Relación con la tabla `Prediction`.
    """

    __tablename__ = "prices_cluster"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, unique=True)

    kmeans_cluster = Column(Integer, nullable=False)  # Clúster asignado por KMeans
    dbscan_cluster = Column(Integer, nullable=False)  # Clúster asignado por DBSCAN

    # Relación con la tabla `Prediction`
    prediction = relationship("Prediction", back_populates="model1_result")


# 🚀 Tabla de Resultados del Modelo 2 (Random Forest, SVM, MLP)
class PricesSegmentation(Base):
    """
    Modelo de base de datos para almacenar los resultados del modelo de segmentación (Random Forest, SVM, MLP).

    Atributos:
        id (UUID): Identificador único del resultado de segmentación.
        prediction_id (UUID): Referencia a la predicción asociada.
        rf_prediction (str): Segmento asignado por Random Forest.
        svm_prediction (str): Segmento asignado por SVM.
        mlp_prediction (str): Segmento asignado por MLP.
        prediction (relationship): Relación con la tabla `Prediction`.
    """

    __tablename__ = "prices_segmentation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, unique=True)

    rf_prediction = Column(String(50), nullable=False)  # Segmento asignado por Random Forest
    svm_prediction = Column(String(50), nullable=False)  # Segmento asignado por SVM
    mlp_prediction = Column(String(50), nullable=False)  # Segmento asignado por MLP

    # Relación con la tabla `Prediction`
    prediction = relationship("Prediction", back_populates="model2_result")


# 🚀 Tabla de Resultados del Modelo 3 (Random Forest, XGBoost, DNN)
class PricesPrediction(Base):
    """
    Modelo de base de datos para almacenar los resultados del modelo de predicción de precios 
    utilizando Random Forest, XGBoost y Deep Neural Networks (DNN).

    Atributos:
        id (UUID): Identificador único del resultado de predicción.
        prediction_id (UUID): Referencia a la predicción asociada.
        rf_prediction (float): Precio estimado por Random Forest.
        xgb_prediction (float): Precio estimado por XGBoost.
        dnn_prediction (float): Precio estimado por Deep Neural Network.
        prediction (relationship): Relación con la tabla `Prediction`.
    """

    __tablename__ = "prices_prediction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, unique=True)

    rf_prediction = Column(Float, nullable=False)  # Precio estimado por Random Forest
    xgb_prediction = Column(Float, nullable=False)  # Precio estimado por XGBoost
    dnn_prediction = Column(Float, nullable=False)  # Precio estimado por Deep Neural Network

    # Relación con la tabla `Prediction`
    prediction = relationship("Prediction", back_populates="model3_result")
