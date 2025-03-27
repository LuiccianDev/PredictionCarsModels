import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import joblib
import pandas as pd
import pathlib
from app.utils import logger
#from models.handlers.save_to_json import save_prices_segmentation
# ---------------------------
# Funciones para Segmentación (Clasificación de precios de autos)
# ---------------------------

# Definir la ruta base del proyecto, moviéndose cuatro niveles hacia arriba desde el archivo actual
PATH_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent

def load_models_segmentation():
    """
    Carga los modelos de segmentación y preprocesadores desde la carpeta:
    models_cars/model_cars_segmentation/
    
    Retorna un diccionario con los modelos y herramientas de preprocesamiento cargados.
    """
    rf_model = joblib.load(PATH_DIR /"models_cars/model_car_segmentation/rf_classifier.pkl")  # Random Forest
    svm_model = joblib.load(PATH_DIR /"models_cars/model_car_segmentation/svm_classifier.pkl")  # SVM
    mlp_model = joblib.load(PATH_DIR /"models_cars/model_car_segmentation/mlp_classifier.pkl")  # MLP (Red Neuronal)
    scaler = joblib.load(PATH_DIR /"models_cars/model_car_segmentation/scaler_classifier.pkl")  # Escalador de datos
    label_encoders = joblib.load(PATH_DIR /"models_cars/model_car_segmentation/label_encoders.pkl")  # Encoders para variables categóricas
    le_segment = joblib.load(PATH_DIR /"models_cars/model_car_segmentation/labelencoder_price_segment.pkl")  # Encoder para etiquetas de segmentación
    
    return {
        'rf': rf_model,
        'svm': svm_model,
        'mlp': mlp_model,
        'scaler': scaler,
        'label_encoders': label_encoders,
        'le_segment': le_segment
    }

def prices_segmentation(new_car_data):
    """
    Recibe un diccionario con las características del auto y retorna la predicción 
    del segmento de precio (Barato, Medio o Caro) usando modelos de clasificación.
    
    Parámetros:
        new_car_data (dict): Diccionario con las características del auto.
    
    Ejemplo de entrada:
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
    
    Retorna:
        dict: Diccionario con las predicciones de cada modelo de clasificación.
    """
    # Cargar los modelos y preprocesadores
    models = load_models_segmentation()
    df = pd.DataFrame([new_car_data])  # Convertir el diccionario en un DataFrame
    
    # Variables categóricas a transformar
    categorical_columns = ["Brand", "Model", "Fuel_Type", "Transmission"]
    unknown_values = {}  # Diccionario para almacenar valores no reconocidos
    
    # Verificar si hay valores desconocidos en las variables categóricas
    for col in categorical_columns:
        if df[col][0] not in models['label_encoders'][col].classes_:
            unknown_values[col] = df[col][0]
    
    # Si hay valores desconocidos, detener la predicción y registrar advertencia
    if unknown_values:
        logger.warning(f"⚠️ Valores desconocidos detectados: {unknown_values}")
        #save_prices_segmentation(new_car_data)
        return None
    
    # Aplicar la transformación de las variables categóricas solo si son conocidas
    for col in categorical_columns:
        df[col] = models['label_encoders'][col].transform(df[col])
    
    # Normalizar los datos numéricos
    df_scaled = models['scaler'].transform(df)
    
    # Realizar predicciones con cada modelo de clasificación
    rf_pred = models['rf'].predict(df_scaled)[0]  # Random Forest
    svm_pred = models['svm'].predict(df_scaled)[0]  # Support Vector Machine
    mlp_pred = models['mlp'].predict(df_scaled)[0]  # Multi-Layer Perceptron
    
    # Convertir las predicciones numéricas a etiquetas originales
    rf_label = models['le_segment'].inverse_transform([rf_pred])[0]
    svm_label = models['le_segment'].inverse_transform([svm_pred])[0]
    mlp_label = models['le_segment'].inverse_transform([mlp_pred])[0]
    
    return {
        'rf': rf_label,
        'svm': svm_label,
        'mlp': mlp_label
    }