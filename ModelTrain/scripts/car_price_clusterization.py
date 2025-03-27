# models/scripts/car_price_clusterization.py

import pandas as pd
import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import pathlib
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from ModelTrain.utils.logger import logger

def load_data(data_path):
    logger.info("Cargando dataset para clusterización...")
    return pd.read_csv(data_path)

def preprocess_data(df):
    logger.info("Preprocesando datos...")
    
    # Verificar valores nulos
    df = df.dropna()
    
    # Convertir columnas categóricas a tipo string para evitar problemas con valores numéricos
    categorical_features = ['Brand', 'Fuel_Type', 'Transmission']
    df[categorical_features] = df[categorical_features].astype(str)
    
    # Aplicar One-Hot Encoding a 'Brand', 'Fuel_Type' y 'Transmission'
    encoder = OneHotEncoder(drop='first', sparse_output=False)
    encoded_features = encoder.fit_transform(df[categorical_features])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
    
    # Aplicar Label Encoding a 'Model'
    label_encoder = LabelEncoder()
    df['Model'] = label_encoder.fit_transform(df['Model'].astype(str))
    
    # Concatenar las columnas procesadas al DataFrame original y eliminar las categóricas originales
    df = pd.concat([df.drop(columns=categorical_features), encoded_df], axis=1)
    
    return df, encoder, label_encoder

def train_clustering_models(df, base_save_path="models_cars"):
    logger.info("Entrenando modelos de clusterización...")
    
    df, encoder, label_encoder = preprocess_data(df)
    
    # Seleccionar las características para clusterización
    X = df.drop(columns=["Price"], errors='ignore')  # Asegúrate de no incluir la variable objetivo
    
    # Escalar los datos antes de la clusterización
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Aplicar PCA para reducción de dimensionalidad
    pca = PCA(n_components=5, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Aplicar K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(X_pca)
    df["Cluster_KMeans"] = kmeans.labels_
    
    # Aplicar DBSCAN
    dbscan = DBSCAN(eps=0.8, min_samples=10)
    df["Cluster_DBSCAN"] = dbscan.fit_predict(X_pca)
    
    # Guardar los modelos
    clustering_dir = os.path.join(base_save_path, "model_car_clusterization")
    pathlib.Path(clustering_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(kmeans, os.path.join(clustering_dir, "kmeans_cluster.pkl"))
    joblib.dump(dbscan, os.path.join(clustering_dir, "dbscan_cluster.pkl"))
    joblib.dump(scaler, os.path.join(clustering_dir, "scaler_cluster.pkl"))
    joblib.dump(pca, os.path.join(clustering_dir, "pca_cluster.pkl"))
    joblib.dump(encoder, os.path.join(clustering_dir, "encoder.pkl"))
    joblib.dump(label_encoder, os.path.join(clustering_dir, "encoder_model.pkl"))
    
    logger.info("\u2705 Modelos de clusterización guardados exitosamente.")

def training_and_save_clusterization_models(data_path, base_save_path="models_cars"):
    df = load_data(data_path)
    train_clustering_models(df, base_save_path)
    logger.info("\u2705 Modelos de clusterización entrenados y guardados correctamente.")
