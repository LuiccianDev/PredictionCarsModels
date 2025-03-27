import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import joblib
import pandas as pd
from ModelTrain.handlers.save_to_json import save_prices_segmentation
# ---------------------------
# Funciones para Segmentación (Clasificación)
# ---------------------------
def load_models_segmentation():
    """
    Carga los modelos de segmentación y preprocesadores desde:
    models_cars/model_cars_segmentation/
    """
    rf_model = joblib.load("models_cars/model_car_segmentation/rf_classifier.pkl")
    svm_model = joblib.load("models_cars/model_car_segmentation/svm_classifier.pkl")
    mlp_model = joblib.load("models_cars/model_car_segmentation/mlp_classifier.pkl")
    scaler = joblib.load("models_cars/model_car_segmentation/scaler_classifier.pkl")
    label_encoders = joblib.load("models_cars/model_car_segmentation/label_encoders.pkl")
    le_segment = joblib.load("models_cars/model_car_segmentation/labelencoder_price_segment.pkl")
    
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
    del segmento de precio (Barato, Medio o Caro) usando los modelos de clasificación.
    
    Ejemplo de new_car_data:
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
    models = load_models_segmentation()
    df = pd.DataFrame([new_car_data])
    
    # Codificar variables categóricas utilizando los codificadores guardados
    categorical_columns = ["Brand", "Model", "Fuel_Type", "Transmission"]
    unknown_values = {}
    
    for col in categorical_columns:
        if df[col][0] not in models['label_encoders'][col].classes_:
            unknown_values[col] = df[col][0]
    
    # Si hay valores desconocidos, guardarlos y no predecir
    if unknown_values:
        print(f"⚠️ Valores desconocidos detectados: {unknown_values}")
        save_prices_segmentation(new_car_data)
        return None
    
    # Aplicar la transformación solo si todos los valores son conocidos
    for col in categorical_columns:
        df[col] = models['label_encoders'][col].transform(df[col])
    
    # Normalizar los datos
    df_scaled = models['scaler'].transform(df)
    
    # Realizar predicciones con cada modelo
    rf_pred = models['rf'].predict(df_scaled)[0]
    svm_pred = models['svm'].predict(df_scaled)[0]
    mlp_pred = models['mlp'].predict(df_scaled)[0]
    
    # Convertir las predicciones numéricas a etiquetas originales
    rf_label = models['le_segment'].inverse_transform([rf_pred])[0]
    svm_label = models['le_segment'].inverse_transform([svm_pred])[0]
    mlp_label = models['le_segment'].inverse_transform([mlp_pred])[0]
    
    return {
        'rf': rf_label,
        'svm': svm_label,
        'mlp': mlp_label
    }
