from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional, Union

# 📌 Importaciones:
# - `BaseModel`: Clase base de Pydantic para la validación de datos.
# - `Field`: Permite definir atributos con valores predeterminados y ejemplos.
# - `ConfigDict`: Configuración para modelos Pydantic (por ejemplo, convertir objetos ORM a modelos).
# - `Dict, Optional, Union`: Tipos de datos para mayor flexibilidad en los esquemas.


# 🔹 Esquema para la petición: datos de entrada para la predicción.
class PredictionRequest(BaseModel):
    """
    Modelo que define los datos de entrada requeridos para hacer una predicción.
    
    Atributos:
    - Brand (str): Marca del vehículo.
    - Model (str): Modelo del vehículo.
    - Year (int): Año de fabricación.
    - Engine_Size (float): Tamaño del motor en litros.
    - Fuel_Type (str): Tipo de combustible.
    - Transmission (str): Tipo de transmisión (Manual o Automática).
    - Mileage (int): Kilometraje recorrido.
    - Doors (int): Número de puertas.
    - Owner_Count (int): Número de propietarios anteriores.

    Ejemplo:
    {
        "Brand": "Toyota",
        "Model": "RAV4",
        "Year": 2006,
        "Engine_Size": 1.3,
        "Fuel_Type": "Hybrid",
        "Transmission": "Manual",
        "Mileage": 195129,
        "Doors": 4,
        "Owner_Count": 5
    }
    """
    Brand: str = Field(..., example="Toyota")
    Model: str = Field(..., example="RAV4")
    Year: int = Field(..., example=2006)
    Engine_Size: float = Field(..., example=1.3)
    Fuel_Type: str = Field(..., example="Hybrid")
    Transmission: str = Field(..., example="Manual")
    Mileage: int = Field(..., example=195129)
    Doors: int = Field(..., example=4)
    Owner_Count: int = Field(..., example=5)


# 🔹 Esquema para los resultados del modelo 1 (PricesCluster)
class PricesClusterResult(BaseModel):
    """
    Modelo para representar los resultados de la predicción basada en clustering.
    
    Atributos:
    - kmeans_cluster (int): Etiqueta del clúster asignado por el modelo K-Means.
    - dbscan_cluster (int): Etiqueta del clúster asignado por el modelo DBSCAN.
    """
    kmeans_cluster: int
    dbscan_cluster: int

    model_config = ConfigDict(from_attributes=True)


# 🔹 Esquema para los resultados del modelo 2 (PricesSegmentation)
class PricesSegmentationResult(BaseModel):
    """
    Modelo para representar los resultados de la predicción basada en segmentación.
    
    Atributos:
    - rf_prediction (str): Predicción realizada por Random Forest.
    - svm_prediction (str): Predicción realizada por Support Vector Machine (SVM).
    - mlp_prediction (str): Predicción realizada por Multi-Layer Perceptron (MLP).
    """
    rf_prediction: str
    svm_prediction: str
    mlp_prediction: str

    model_config = ConfigDict(from_attributes=True)


# 🔹 Esquema para los resultados del modelo 3 (PricesPrediction)
class PricesPredictionResult(BaseModel):
    """
    Modelo para representar los resultados de la predicción basada en estimación de precios.
    
    Atributos:
    - rf_prediction (float): Predicción de precio realizada por Random Forest.
    - xgb_prediction (float): Predicción de precio realizada por XGBoost.
    - dnn_prediction (float): Predicción de precio realizada por una red neuronal profunda (DNN).
    """
    rf_prediction: float
    xgb_prediction: float
    dnn_prediction: float

    model_config = ConfigDict(from_attributes=True)


# 🔹 Esquema para la respuesta de predicción.
class PredictionResponse(BaseModel):
    """
    Modelo que define la estructura de la respuesta para una predicción.
    
    Atributos:
    - model (str): Nombre del modelo utilizado para la predicción.
    - prediction (Union[PricesClusterResult, PricesSegmentationResult, PricesPredictionResult]):
      Resultado de la predicción, que puede pertenecer a cualquiera de los tres modelos definidos.
    """
    model: str
    prediction: Union[PricesClusterResult, PricesSegmentationResult, PricesPredictionResult]

    model_config = ConfigDict(from_attributes=True)
