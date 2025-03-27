import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import joblib
import pandas as pd
from ModelTrain.utils.logger  import logger
from ModelTrain.handlers.save_to_json import save_prices_clusterization
# ---------------------------
# Funciones para Clusterización
# ---------------------------
def load_models_clusterization():
    """
    Carga los modelos de clustering desde:
    models_cars/model_car_clusterization/
    """
    try:
        kmeans = joblib.load("models_cars/model_car_clusterization/kmeans_cluster.pkl")
        dbscan = joblib.load("models_cars/model_car_clusterization/dbscan_cluster.pkl")
        scaler = joblib.load("models_cars/model_car_clusterization/scaler_cluster.pkl")
        pca = joblib.load("models_cars/model_car_clusterization/pca_cluster.pkl")
        encoder = joblib.load("models_cars/model_car_clusterization/encoder.pkl")  # OneHotEncoder
        label_encoder = joblib.load("models_cars/model_car_clusterization/encoder_model.pkl")  # LabelEncoder
        
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
    Recibe un diccionario con las características del auto y retorna la asignación de clusters
    utilizando K-Means y DBSCAN.
    """
    try:
        # Cargar modelos y encoders
        clustering_models = load_models_clusterization()
        if clustering_models is None:
            raise RuntimeError("No se pudieron cargar los modelos de clusterización.")
        
        # Convertir el diccionario a DataFrame
        df = pd.DataFrame([new_car_data])
        
        # Verificar que todas las columnas necesarias están presentes
        required_columns = ["Brand", "Model", "Fuel_Type", "Transmission", "Year", "Engine_Size", "Mileage", "Doors", "Owner_Count"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Faltan las siguientes columnas: {missing_columns}")

        # 🔹 Lista para guardar valores desconocidos
        unseen_data = {}

        # Codificar la columna "Model" con LabelEncoder
        try:
            if df["Model"].iloc[0] not in clustering_models["label_encoder"].classes_:
                unseen_data["Model"] = df["Model"].iloc[0]
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
                    unseen_data[col] = df[col].iloc[0]
            
            if unseen_data:
                logger.warning(f"Valores desconocidos en OneHotEncoder: {unseen_data}. Se requiere actualizar el encoder.")
                save_prices_clusterization(new_car_data)
                return {"kmeans": None, "dbscan": None}

            encoded_df = pd.DataFrame(clustering_models["encoder"].transform(df[categorical_columns]),
                                      columns=clustering_models["encoder"].get_feature_names_out(categorical_columns))
        except Exception as e:
            logger.exception(f"Error al aplicar OneHotEncoder: {e}")
            raise
        
        df = df.drop(columns=categorical_columns).reset_index(drop=True)
        df = pd.concat([df, encoded_df], axis=1)
        
        # Normalizar usando el escalador y aplicar PCA
        try:
            df_scaled = clustering_models['scaler'].transform(df)
            df_pca = clustering_models['pca'].transform(df_scaled)
        except Exception as e:
            logger.exception(f"Error en la normalización o PCA: {e}")
            raise
        
        # Obtener la asignación de clusters
        kmeans_cluster = clustering_models['kmeans'].predict(df_pca)[0]
        dbscan_labels = clustering_models['dbscan'].fit_predict(df_pca)
        dbscan_cluster = int(dbscan_labels[0]) if len(dbscan_labels) > 0 else None

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