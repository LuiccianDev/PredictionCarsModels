import os
# Limita el número de CPU utilizadas por joblib para evitar un consumo excesivo de recursos
os.environ["LOKY_MAX_CPU_COUNT"] = "2"

import joblib  # Librería para cargar y guardar modelos de machine learning
import pandas as pd  # Librería para manipulación de datos en formato DataFrame
from app.utils import logger  # Importación del logger para registrar eventos y errores
import pathlib  # Manejo de rutas de archivos
#from models.handlers.save_to_json import save_prices_clusterization

# ---------------------------
# Funciones para Clusterización de precios de autos
# ---------------------------

# Definir la ruta base del proyecto, moviéndose cuatro niveles hacia arriba desde el archivo actual
PATH_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
def load_models_clusterization():
    """
    Carga los modelos de clustering desde el directorio:
    models_cars/model_car_clusterization/

    Retorna un diccionario con los modelos cargados o None en caso de error.
    """
    try:
        # Cargar modelos entrenados previamente con joblib
        kmeans = joblib.load(PATH_DIR / "models_cars/model_car_clusterization/kmeans_cluster.pkl")  # Modelo K-Means
        dbscan = joblib.load(PATH_DIR / "models_cars/model_car_clusterization/dbscan_cluster.pkl")  # Modelo DBSCAN
        scaler = joblib.load(PATH_DIR / "models_cars/model_car_clusterization/scaler_cluster.pkl")  # Escalador de datos
        pca = joblib.load(PATH_DIR / "models_cars/model_car_clusterization/pca_cluster.pkl")  # Reducción de dimensionalidad con PCA
        encoder = joblib.load(PATH_DIR / "models_cars/model_car_clusterization/encoder.pkl")  # OneHotEncoder para variables categóricas
        label_encoder = joblib.load(PATH_DIR / "models_cars/model_car_clusterization/encoder_model.pkl")  # LabelEncoder para modelos de autos
        
        logger.info("Modelos de clusterización cargados correctamente.")

        return {
            'kmeans': kmeans,
            'dbscan': dbscan,
            'scaler': scaler,
            'pca': pca,
            'encoder': encoder,
            'label_encoder': label_encoder
        }
    except Exception as e:
        logger.exception("Error al cargar los modelos de clusterización")
        return None
def prices_clusterization(new_car_data):
    """
    Asigna un auto a clusters usando modelos de clustering (K-Means y DBSCAN).

    Parámetros:
        new_car_data (dict): Diccionario con las características del auto.

    Retorna:
        dict: Resultado con los clusters asignados por K-Means y DBSCAN.
    """
    try:
        # Cargar modelos y encoders
        clustering_models = load_models_clusterization()
        if clustering_models is None:
            raise RuntimeError("No se pudieron cargar los modelos de clusterización.")
        
        # Convertir el diccionario de entrada en un DataFrame de Pandas
        df = pd.DataFrame([new_car_data])
        
        # Verificar que todas las columnas necesarias están presentes
        required_columns = ["Brand", "Model", "Fuel_Type", "Transmission", "Year", "Engine_Size", "Mileage", "Doors", "Owner_Count"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Faltan las siguientes columnas: {missing_columns}")

        # 🔹 Diccionario para almacenar valores no vistos previamente en los encoders
        unseen_data = {}

        # Codificar la columna "Model" con LabelEncoder
        try:
            if df["Model"].iloc[0] not in clustering_models["label_encoder"].classes_:
                unseen_data["Model"] = df["Model"].iloc[0]  # Guardar modelo no visto
            else:
                df["Model"] = clustering_models["label_encoder"].transform(df["Model"])
        except Exception as e:
            logger.exception(f"Error al codificar la columna 'Model': {e}")
            raise
        
        # Aplicar OneHotEncoder a las variables categóricas
        categorical_columns = ["Brand", "Fuel_Type", "Transmission"]
        try:
            for col in categorical_columns:
                if df[col].iloc[0] not in clustering_models["encoder"].categories_[categorical_columns.index(col)]:
                    unseen_data[col] = df[col].iloc[0]  # Guardar valores desconocidos
            
            # Si hay valores desconocidos, registrar advertencia y retornar None
            if unseen_data:
                logger.warning(f"Valores desconocidos en OneHotEncoder: {unseen_data}. Se requiere actualizar el encoder.")
                # save_prices_clusterization(new_car_data)
                return {"kmeans": None, "dbscan": None}

            # Transformar las variables categóricas usando OneHotEncoder
            encoded_df = pd.DataFrame(clustering_models["encoder"].transform(df[categorical_columns]),
                                      columns=clustering_models["encoder"].get_feature_names_out(categorical_columns))
        except Exception as e:
            logger.exception(f"Error al aplicar OneHotEncoder: {e}")
            raise
        
        # Eliminar las columnas categóricas originales y concatenar las codificadas
        df = df.drop(columns=categorical_columns).reset_index(drop=True)
        df = pd.concat([df, encoded_df], axis=1)
        
        # Normalizar los datos y aplicar PCA para reducción de dimensionalidad
        try:
            df_scaled = clustering_models['scaler'].transform(df)  # Normalización
            df_pca = clustering_models['pca'].transform(df_scaled)  # Transformación PCA
        except Exception as e:
            logger.exception(f"Error en la normalización o PCA: {e}")
            raise
        
        # Obtener la asignación de clusters
        kmeans_cluster = clustering_models['kmeans'].predict(df_pca)[0]  # Predicción con K-Means
        dbscan_labels = clustering_models['dbscan'].fit_predict(df_pca)  # Predicción con DBSCAN
        dbscan_cluster = int(dbscan_labels[0]) if len(dbscan_labels) > 0 else None  # Asignación de cluster DBSCAN

        return {
            'kmeans': int(kmeans_cluster),
            'dbscan': int(dbscan_cluster) if dbscan_cluster is not None else None
        }

    except Exception as e:
        logger.error(f"Error en prices_clusterization: {e}")
        return {
            'kmeans': None,
            'dbscan': None
        }