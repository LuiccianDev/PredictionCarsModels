import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import joblib
import pandas as pd
from tensorflow import keras
#from models.handlers.save_to_json import save_prices_prediction
from app.utils import logger
import pathlib
PATH_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
def load_models():
    """
    Carga los modelos de predicción (Random Forest, XGBoost y DNN),
    el escalador y los codificadores de etiquetas desde la carpeta de modelos.
    """
    rf_model = joblib.load(PATH_DIR / "models_cars/model_cars_prediction_prices/random_forest_model.pkl")
    xgb_model = joblib.load(PATH_DIR / "models_cars/model_cars_prediction_prices/xgboost_model.pkl")
    dnn_model = keras.models.load_model(PATH_DIR / "models_cars/model_cars_prediction_prices/dnn_model.h5", compile=False)
    
    scaler = joblib.load(PATH_DIR / "models_cars/model_cars_prediction_prices/scaler.pkl")
    label_encoders = joblib.load(PATH_DIR / "models_cars/model_cars_prediction_prices/label_encoders.pkl")
    
    return {
        'rf': rf_model,
        'xgb': xgb_model,
        'dnn': dnn_model,
        'scaler': scaler,
        'label_encoders': label_encoders
    }

def prices_prediction(new_car_data):
    """
    Realiza la predicción del precio de un auto usando los modelos cargados.
    
    Parámetro:
        new_car_data (dict): Diccionario con las características del auto. Ejemplo:
            { "Brand": "Mercedes",
              "Model": "E-Class",
              "Year": 2004,
              "Engine_Size": 4.9,
              "Fuel_Type": "Petrol",
              "Transmission": "Semi-Automatic",
              "Mileage": 175273,
              "Doors": 3,
              "Owner_Count": 5 }
    
    Retorna:
        dict: Predicciones de precio de cada modelo.
    """
    models = load_models()
    
    # Convertir el diccionario a DataFrame
    new_data = pd.DataFrame([new_car_data])
    
    # Codificar variables categóricas usando los codificadores cargados
    categorical_columns = ["Brand", "Model", "Fuel_Type", "Transmission"]
    unknown_values = {}
    
    
    for col in categorical_columns:
        if new_data[col][0] not in models['label_encoders'][col].classes_:
            unknown_values[col] = new_data[col][0]
    
    
    # Si hay valores desconocidos, guardarlos y no predecir
    if unknown_values:
        logger.info(f"⚠️ Valores desconocidos detectados: {unknown_values}")
        #save_prices_prediction(new_car_data)
        return None
    
    # Aplicar la transformación solo si todos los valores son conocidos
    for col in categorical_columns:
        new_data[col] = models['label_encoders'][col].transform(new_data[col])
        
    # Normalizar los datos usando el escalador cargado
    new_data_scaled = models['scaler'].transform(new_data)
    
    # Realizar las predicciones con cada modelo
    rf_prediction = models['rf'].predict(new_data_scaled)[0].item()
    xgb_prediction = models['xgb'].predict(new_data_scaled)[0].item()
    dnn_prediction = models['dnn'].predict(new_data_scaled)[0][0].item()
    
    return {
        'rf': round(rf_prediction,3),
        'xgb': round(xgb_prediction,3),
        'dnn': round(dnn_prediction,3), #dnn_prediction
    }