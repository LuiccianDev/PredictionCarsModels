import pandas as pd
import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"
import pathlib
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from ModelTrain.utils.logger import logger


def load_data(file_path):
    logger.info("Cargando dataset para segmentación...")
    return pd.read_csv(file_path)

def preprocess_data(df):
    logger.info("Preprocesando datos para segmentación...")
    categorical_columns = ['Brand', 'Model', 'Fuel_Type', 'Transmission']
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    price_quantiles = df["Price"].quantile([0.33, 0.66])
    df["Price_Segment"] = df["Price"].apply(
        lambda price: "Barato" if price <= price_quantiles.loc[0.33] else (
            "Medio" if price <= price_quantiles.loc[0.66] else "Caro"
        )
    )
    return df, label_encoders

def create_price_segment_encoder(df):
    # Crear un LabelEncoder para la columna Price_Segment
    le_segment = LabelEncoder()
    le_segment.fit(df["Price_Segment"])
    return le_segment

def prepare_classification_data(df):
    X = df.drop(columns=["Price", "Price_Segment"])
    le_y = LabelEncoder()
    y = le_y.fit_transform(df["Price_Segment"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_random_forest(X_train, y_train):
    logger.info("Entrenando Random Forest para segmentación...")
    model = RandomForestClassifier(n_estimators=300, max_depth=20, min_samples_split=5, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_svm(X_train, y_train):
    logger.info("Entrenando SVM para segmentación...")
    model = SVC(kernel='rbf', C=10, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_mlp(X_train, y_train):
    logger.info("Entrenando MLP para segmentación...")
    model = MLPClassifier(hidden_layer_sizes=(128, 128), max_iter=500, activation='relu', solver='adam', random_state=42)
    model.fit(X_train, y_train)
    return model

def save_segmentation_models(models, scaler, label_encoders, le_segment, base_save_path):
    logger.info("Guardando modelos de segmentación...")
    segmentation_dir = os.path.join(base_save_path, "model_car_segmentation")
    pathlib.Path(segmentation_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(models['rf_classifier'], os.path.join(segmentation_dir, "rf_classifier.pkl"))
    joblib.dump(models['svm_classifier'], os.path.join(segmentation_dir, "svm_classifier.pkl"))
    joblib.dump(models['mlp_classifier'], os.path.join(segmentation_dir, "mlp_classifier.pkl"))
    joblib.dump(scaler, os.path.join(segmentation_dir, "scaler_classifier.pkl"))
    joblib.dump(label_encoders, os.path.join(segmentation_dir, "label_encoders.pkl"))
    # Guardar el encoder para Price_Segment
    joblib.dump(le_segment, os.path.join(segmentation_dir, "labelencoder_price_segment.pkl"))
    logger.info("✅ Modelos de segmentación guardados exitosamente.")

def training_and_save_segmentation_models(data_path, base_save_path="models_cars"):
    df = load_data(data_path)
    df, label_encoders = preprocess_data(df)
    le_segment = create_price_segment_encoder(df)
    X_train, X_test, y_train, y_test, scaler = prepare_classification_data(df)
    models = {
        'rf_classifier': train_random_forest(X_train, y_train),
        'svm_classifier': train_svm(X_train, y_train),
        'mlp_classifier': train_mlp(X_train, y_train)
    }
    for name, model in models.items():
        acc = accuracy_score(y_test, model.predict(X_test))
        logger.info(f"{name} Accuracy: {acc:.4f}")
    save_segmentation_models(models, scaler, label_encoders, le_segment, base_save_path)
    logger.info("✅ Modelos de segmentación entrenados y guardados correctamente.")

# Ejemplo de uso (para pruebas locales)
if __name__ == "__main__":
    DATASET_PATH = "data/car_price_dataset.csv"
    BASE_SAVE_PATH = "models_cars"
    training_and_save_segmentation_models(DATASET_PATH, BASE_SAVE_PATH)



""" Cluster 0: Autos económicos con motor pequeño.
    Cluster 1: Autos medianos con buen rendimiento.
    Cluster 2: Autos de lujo con alto precio.
    Cluster 3: SUVs o camionetas con características específicas. """