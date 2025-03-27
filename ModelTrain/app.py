
#! Entrenamintod el modelo de entrenaminto son 3 modelos 
from ModelTrain.scripts.car_price_prediction import training_and_save_prediction_model
from ModelTrain.scripts.car_price_segmentation import training_and_save_segmentation_models
from ModelTrain.scripts.car_price_clusterization import training_and_save_clusterization_models

import pathlib

#! Importar modelos para su utilizacion
from ModelTrain.utils.load_model_prices_segmetation import prices_segmentation
from ModelTrain.utils.load_model_prices_clusterization import prices_clusterization
from ModelTrain.utils.load_models_prices_prediction import prices_prediction 

#! importar utils 
from ModelTrain.validations.data_validation import validate_car_data
from ModelTrain.utils.logger import logger



#* Entrenar el modelo para su usos posterior
def train_models():
    
    DATASET_PATH = pathlib.Path(__file__).resolve().parent / "data" / "car_price_dataset.csv"
    BASE_SAVE_PATH = pathlib.Path(__file__).resolve().parent / "models_cars"

    training_and_save_prediction_model(DATASET_PATH, BASE_SAVE_PATH)

    #* Entrenar y guardar modelos de segmentación (clasificación)
    training_and_save_segmentation_models(DATASET_PATH, BASE_SAVE_PATH)

    #* Entrenar y guardar modelos de clusterización
    training_and_save_clusterization_models(DATASET_PATH, BASE_SAVE_PATH)

#! predeccion multiple datos 
def multiply_test_model():
    new_cars = [
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
        },
        {
            "Brand": "Ford",
            "Model": "Focus",
            "Year": 2012,
            "Engine_Size": 1.6,
            "Fuel_Type": "Gasoline",
            "Transmission": "Automatic",
            "Mileage": 120000,
            "Doors": 4,
            "Owner_Count": 3
        },
        {
            "Brand": "Honda",
            "Model": "Civic",
            "Year": 2015,
            "Engine_Size": 2.0,
            "Fuel_Type": "Gasoline",#! No hay gasolinele label ene ls entrenemainto 
            "Transmission": "Manual",
            "Mileage": 85000,
            "Doors": 4,
            "Owner_Count": 2
        },
        {
            "Brand": "BMW", #! no ha ene nl mdoelo lols dsatos de BNW
            "Model": "X5",
            "Year": 2018,
            "Engine_Size": 3.0,
            "Fuel_Type": "Diesel",
            "Transmission": "Automatic",
            "Mileage": 60000,
            "Doors": 5,
            "Owner_Count": 1
        },
        {
            "Brand": "Tesla", #! no ha ene nl mdoelo lols dsatos de tesla 
            "Model": "Model 3",
            "Year": 2021,
            "Engine_Size": 0.0,
            "Fuel_Type": "Electric",
            "Transmission": "Automatic",
            "Mileage": 30000,
            "Doors": 4,
            "Owner_Count": 1
        }
    ]
    for i, car in enumerate(new_cars, start=1):
        try:
            validated_car = validate_car_data(car)  # Validar datos
        except ValueError as e:
            logger.warning(f"⚠️ Auto {i} ({car.get('Brand', 'Desconocido')} {car.get('Model', 'Desconocido')}) omitido: {e}")
            continue  # Saltar este auto y continuar con los siguientes
        print(f"\n🚗 **Predicción para Auto {i} ({car['Brand']} {car['Model']})**")
        preds = prices_prediction(car)
        print("🔹 Predicciones:", preds)

        seg_pred = prices_segmentation(car)
        print("🔹 Predicción de segmentación:", seg_pred)

        clu_pred = prices_clusterization(car)
        print("🔹 Predicción de clusterización:", clu_pred)


#! predecir un datos para su suos 
def test_model():
    new_car = {
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
    preds = prices_prediction(new_car)
    print("Predicciones:", preds)

    seg_pred = prices_segmentation(new_car)
    print("Predicción de segmentación:", seg_pred)
        
    clu_pred = prices_clusterization(new_car)
    print("Predicción de clusterización:", clu_pred)
    


