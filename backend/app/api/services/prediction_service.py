from typing import Dict
import uuid
from app.api.schemas.prediction_schema import (PredictionRequest,
                                               PricesClusterResult, 
                                               PricesSegmentationResult, 
                                               PricesPredictionResult)
from app.utils import (prices_clusterization, 
                       prices_prediction, 
                       prices_segmentation)
from sqlalchemy.orm import Session


# Importar modelos de base de datos
from app.models import (
    Prediction,
    PricesCluster,
    PricesPrediction,
    PricesSegmentation,
)

# 🔹 Funciones de predicción
def predict_clusterization(data: Dict) -> Dict:
    """
    Ejecuta la función de clusterización de precios.
    Modelo 3: devuelve un diccionario con los resultados de clusterización, por ejemplo:
    {"kmeans": valor, "dbscan": valor}
    """
    return prices_clusterization(data)

def predict_segmentation(data: Dict) -> Dict:
    """
    Ejecuta la función de segmentación de precios.
    Modelo 2: devuelve un diccionario con los resultados de segmentación, por ejemplo:
    {"rf": valor, "svm": valor, "mlp": valor}
    """
    return prices_segmentation(data)

def predict_prices(data: Dict) -> Dict:
    """
    Ejecuta la función de predicción de precios.
    Modelo 1: devuelve un diccionario con los resultados de predicción, por ejemplo:
    {"rf": valor, "xgb": valor, "dnn": valor}
    """
    return prices_prediction(data)

# 🔹 Mapeo entre modelos y funciones
MODEL_FUNCTIONS = {
    "model1": predict_prices,
    "model2": predict_segmentation,
    "model3": predict_clusterization,
}

def is_duplicated_prediction(db: Session, user_id: str, request: PredictionRequest):
    """
    Devuelve la predicción existente (si la hay) o None.
    Se compara la información de entrada y el user_id.
    """
    return db.query(Prediction).filter(
        Prediction.user_id == user_id,
        Prediction.brand == request.Brand,
        Prediction.model == request.Model,
        Prediction.year == request.Year,
        Prediction.engine_size == request.Engine_Size,
        Prediction.fuel_type == request.Fuel_Type,
        Prediction.transmission == request.Transmission,
        Prediction.mileage == request.Mileage,
        Prediction.doors == request.Doors,
        Prediction.owner_count == request.Owner_Count
    ).first()

def save_prediction(user_id: str, request: PredictionRequest, db: Session, model_name: str) -> Dict:
    """
    Guarda la predicción y el resultado del modelo en la base de datos.
    Si ya existe una predicción con los mismos datos para el mismo user_id, no se guarda de nuevo.
    Además, si ya existe un registro del resultado para el modelo en esa predicción, no se guarda duplicado,
    sino que se devuelve el registro existente.
    Retorna un diccionario resultado del modelo.
    """
    func = MODEL_FUNCTIONS.get(model_name)
    if not func:
        raise ValueError(f"Modelo '{model_name}' no es válido. Debe ser 'model1', 'model2' o 'model3'.")

    # Ejecutar la predicción para obtener el resultado del modelo
    result_predic = func(request.model_dump())
    input_data = request.model_dump()

    # Verificar si ya existe una predicción con los mismos datos para ese usuario
    existing_prediction = is_duplicated_prediction(db, user_id, request)
    
    if existing_prediction:
        # La predicción ya existe, consultamos si ya se guardó el resultado del modelo
        if model_name == "model1":
            existing_result = db.query(PricesPrediction).filter(PricesPrediction.prediction_id == existing_prediction.id).first()
            if existing_result:
                response = PricesPredictionResult.model_validate(existing_result)
                return response.model_dump()
        elif model_name == "model2":
            existing_result = db.query(PricesSegmentation).filter(PricesSegmentation.prediction_id == existing_prediction.id).first()
            if existing_result:
                response = PricesSegmentationResult.model_validate(existing_result)
                return response.model_dump()
        elif model_name == "model3":
            existing_result = db.query(PricesCluster).filter(PricesCluster.prediction_id == existing_prediction.id).first()
            if existing_result:
                response = PricesClusterResult.model_validate(existing_result)
                return response.model_dump()
        # Si la predicción existe pero no hay resultado del modelo, usaremos la predicción existente para guardar el nuevo resultado.
        prediction_db = existing_prediction
    else:
        # No existe la predicción: se crea una nueva
        prediction_db = Prediction(
            id=uuid.uuid4(),  # Generamos un UUID para la predicción
            user_id=user_id,  # Id del usuario que realizó la predicción
            brand=input_data.get("Brand"),
            model=input_data.get("Model"),
            year=input_data.get("Year"),
            engine_size=input_data.get("Engine_Size"),
            fuel_type=input_data.get("Fuel_Type"),
            transmission=input_data.get("Transmission"),
            mileage=input_data.get("Mileage"),
            doors=input_data.get("Doors"),
            owner_count=input_data.get("Owner_Count")
        )
        db.add(prediction_db)
        db.commit()
        db.refresh(prediction_db)

    # Según el modelo, se guarda el resultado solo si no existe ya.
    if model_name == "model1":
        new_result = PricesPrediction(
            id=uuid.uuid4(),
            prediction_id=prediction_db.id,
            rf_prediction=result_predic.get("rf"),
            xgb_prediction=result_predic.get("xgb"),
            dnn_prediction=result_predic.get("dnn")
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        response = PricesPredictionResult.model_validate(new_result)
       
    elif model_name == "model2":
        new_result = PricesSegmentation(
            id=uuid.uuid4(),
            prediction_id=prediction_db.id,
            rf_prediction=result_predic.get("rf"),
            svm_prediction=result_predic.get("svm"),
            mlp_prediction=result_predic.get("mlp")
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        response = PricesSegmentationResult.model_validate(new_result)
        
    elif model_name == "model3":
        new_result = PricesCluster(
            id=uuid.uuid4(),
            prediction_id=prediction_db.id,
            kmeans_cluster=result_predic.get("kmeans"),
            dbscan_cluster=result_predic.get("dbscan")
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        response = PricesClusterResult.model_validate(new_result)
    # Ejecutar la predicción para obtener el resultado del modelo
    #result_predic = func(request.model_dump())
    
    return response.model_dump()





""" from typing import Dict

# importar schemas 
from app.api.schemas.prediction_schema import PredictionRequest


# import fucniones de l os modelso de entrenaimineto 
from app.utils.load_model_prices_clusterization import prices_clusterization
from app.utils.load_models_prices_prediction import prices_prediction
from app.utils.load_model_prices_segmetation import prices_segmentation
from sqlalchemy.orm import Session
import uuid

#! importar modelos de bas e de datos 
from app.models.predictions_models import Prediction
from app.models.result_prediction_models import (
    PricesCluster,
    PricesPrediction,
    PricesSegmentation,)

# 🔹 Funciones de predicción
def predict_clusterization(data: Dict) -> Dict:
    #! modelo 3 me devueleve un dicionario de dict(str, int) | dict(str, None)
    # Modelo 3: devuelve un diccionario, por ejemplo {"kmeans": valor, "dbscan": valor}
    return prices_clusterization(data)

def predict_segmentation(data: Dict) -> Dict:
    #! modelo 2 me devuelebve un dicionarionde sdict(str,str)
    # Modelo 2: devuelve un diccionario, por ejemplo {"rf": valor, "svm": valor, "mlp": valor}
    return prices_segmentation(data)

def predict_prices(data: Dict) -> Dict:
    #! modelo 1 me devueleve un dicionariosn de dict(str, float)
    # Modelo 1: devuelve un diccionario, por ejemplo {"rf": valor, "xgb": valor, "dnn": valor}
    return prices_prediction(data)

# 🔹 Mapeo entre modelos y funciones
MODEL_FUNCTIONS = {
    "model1": predict_prices,
    "model2": predict_segmentation,
    "model3": predict_clusterization,
}

def predict(model_name: str, request: PredictionRequest) -> Dict:
    func = MODEL_FUNCTIONS.get(model_name)
    if not func:
        raise ValueError(f"Modelo '{model_name}' no es válido. Debe ser 'model1', 'model2' o 'model3'.")
    
    print(f"Recibiendo datos para {model_name}: {request.model_dump()}")  # Log para depuración
    
    return func(request.model_dump())  # Usar model_dump() en Pydantic v2

def is_duplicated_prediction(db: Session, user_id: str, request: PredictionRequest) -> bool:
    
    return db.query(Prediction).filter(
        Prediction.user_id == user_id,
        Prediction.brand == request.Brand,
        Prediction.model == request.Model,
        Prediction.year == request.Year,
        Prediction.engine_size == request.Engine_Size,
        Prediction.fuel_type == request.Fuel_Type,
        Prediction.transmission == request.Transmission,
        Prediction.mileage == request.Mileage,
        Prediction.doors == request.Doors,
        Prediction.owner_count == request.Owner_Count
    ).first()

def save_prediction(user_id: str, request: PredictionRequest, db: Session, model_name: str) -> Prediction:
    func = MODEL_FUNCTIONS.get(model_name)
    if not func:
        raise ValueError(f"Modelo '{model_name}' no es válido. Debe ser 'model1', 'model2' o 'model3'.")
    
    result_predic = func(request.model_dump())
    
    input_data = request.model_dump()
    
    if is_duplicated_prediction(db, user_id, request):
        raise ValueError("Predicción duplicada. No se puede guardar.")
    
    # Asumamos que los campos del objeto Prediction son:
    # model_name, brand, model, year, engine_size, fuel_type, transmission, mileage, doors, owner_count.
    # Aquí hacemos un mapeo simple:
    prediction_db = Prediction(
        id=uuid.uuid4(),  # Generamos un UUID para la predicción
        user_id=user_id,  # El id del usuario que realizó la predicción
        brand=input_data.get("Brand"),           # o input_data.get("brand") si usas minúsculas
        model=input_data.get("Model"),
        year=input_data.get("Year"),
        engine_size=input_data.get("Engine_Size"),
        fuel_type=input_data.get("Fuel_Type"),
        transmission=input_data.get("Transmission"),
        mileage=input_data.get("Mileage"),
        doors=input_data.get("Doors"),
        owner_count=input_data.get("Owner_Count")
        # Si deseas guardar el resultado global en la misma tabla, puedes agregar un campo "result" de tipo JSON.
        # result=input_data,  # o result=result, según tu diseño.
    )
    
    db.add(prediction_db)
    db.commit()
    db.refresh(prediction_db)
    
    #pr4idic prices
    if model_name == "model1": 
        prices_prediction = PricesPrediction(
            id=uuid.uuid4(),
            prediction_id=prediction_db.id,
            rf_prediction=result_predic.get("rf"),
            xgb_prediction=result_predic.get("xgb"),
            dnn_prediction=result_predic.get("dnn")
        )
        db.add(prices_prediction)
        db.commit()
        db.refresh(prices_prediction)
        
    
    # predict segmenation
    elif model_name == "model2":
        prices_segmentation = PricesSegmentation(
            id=uuid.uuid4(),
            prediction_id=prediction_db.id,
            rf_prediction=result_predic.get("rf"),
            svm_prediction=result_predic.get("svm"),
            mlp_prediction=result_predic.get("mlp")
        )
        db.add(prices_segmentation)
        db.commit()
        db.refresh(prices_segmentation)
            
                
        #'rf': rf_prediction,
        #'xgb': xgb_prediction,
        #'dnn': dnn_prediction 
    # predict cluter     
    elif model_name == "model3":
        prices_clusterization = PricesCluster(
            id=uuid.uuid4(),
            prediction_id=prediction_db.id,
            kmeans_cluster=result_predic.get("kmeans"),  # ✅ Correcto, pertenece a PricesCluster
            dbscan_cluster=result_predic.get("dbscan")   # ✅ Correcto, pertenece a PricesCluster
        )
        db.add(prices_clusterization)
        db.commit()
        db.refresh(prices_clusterization)
 """
    
    
    