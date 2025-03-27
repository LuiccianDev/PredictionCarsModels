import pandas as pd
import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import pathlib
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import r2_score
from ModelTrain.utils.logger  import logger

def load_data(file_path):
    logger.info("Cargando dataset...")
    return pd.read_csv(file_path)

def preprocess_data(df):
    logger.info("Preprocesando datos...")
    categorical_columns = ['Brand', 'Model', 'Fuel_Type', 'Transmission']
    # Ajuste: Crear y aplicar LabelEncoder para cada columna
    label_encoders = {col: LabelEncoder().fit(df[col]) for col in categorical_columns}
    for col, le in label_encoders.items():
        df[col] = le.transform(df[col])
    
    X = df.drop(columns=["Price"])
    y = df["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, scaler, label_encoders

def train_random_forest(X_train, y_train):
    logger.info("Entrenando Random Forest...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_xgboost(X_train, y_train):
    logger.info("Entrenando XGBoost...")
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_dnn(X_train, y_train):
    logger.info("Entrenando DNN...")
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=0)
    return model

def evaluate_model(model, X_test, y_test, model_name):
    if hasattr(model, 'predict'):
        y_pred = model.predict(X_test)
        score = r2_score(y_test, y_pred)
    else:
        loss, mae = model.evaluate(X_test, y_test, verbose=0)
        score = 1 - (loss / (y_test.var() + 1e-9))  # Aproximación de R2 para la DNN
    logger.info(f"{model_name} R^2 Score: {score:.4f}")
    return score




def save_models(models, scaler, label_encoders, base_save_path):
    logger.info("Guardando modelos...")
    # Definir la ruta de guardado para los modelos de predicción
    save_dir = os.path.join(base_save_path, "model_cars_prediction_prices")
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    joblib.dump(models['rf'], os.path.join(save_dir, "random_forest_model.pkl"))
    joblib.dump(models['xgb'], os.path.join(save_dir, "xgboost_model.pkl"))
    models['dnn'].save(os.path.join(save_dir, "dnn_model.h5"))
    joblib.dump(scaler, os.path.join(save_dir, "scaler.pkl"))
    joblib.dump(label_encoders, os.path.join(save_dir, "label_encoders.pkl"))
    logger.info("✅ Modelos guardados exitosamente.")

def training_and_save_prediction_model(data_path, base_save_path):
    df = load_data(data_path)
    X_train, X_test, y_train, y_test, scaler, label_encoders = preprocess_data(df)
    
    models = {
        'rf': train_random_forest(X_train, y_train),
        'xgb': train_xgboost(X_train, y_train),
        'dnn': train_dnn(X_train, y_train)
    }
    
    for name, model in models.items():
        score = evaluate_model(model, X_test, y_test, name.upper())
        logger.info(f"{name.upper()} R^2 Score: {score:.4f}")
    
    save_models(models, scaler, label_encoders, base_save_path)
    logger.info("✅ Todos los modelos han sido entrenados y guardados correctamente.")

# Ejemplo de uso:
# Para ser llamado desde otro script, simplemente importa esta función y pásale la ruta del dataset y la carpeta base de guardado.
# Por ejemplo:
#   from models.scripts.car_price_prediction import training_and_save_model
#   training_and_save_model("data/car_price_dataset.csv", "models_cars")



