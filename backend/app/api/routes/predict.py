from fastapi import APIRouter, HTTPException, Depends
# 📌 Importa `APIRouter` para definir rutas, `HTTPException` para manejar errores HTTP y `Depends` para la inyección de dependencias.

from sqlalchemy.orm import Session
# 📌 Importa `Session` de SQLAlchemy para interactuar con la base de datos.

from app.api.schemas.prediction_schema import PredictionRequest, PredictionResponse
# 📌 Importa los esquemas `PredictionRequest` y `PredictionResponse` para validar las solicitudes y respuestas.

#from app.api.services.prediction_service import predict
# 📌 (Comentado) Importaría la función `predict`, que realizaría una predicción basada en un modelo.

from app.api.services.prediction_service import save_prediction
# 📌 Importa `save_prediction`, que guarda la predicción en la base de datos.

from app.core import get_db
# 📌 Importa `get_db` para obtener la sesión de la base de datos en cada solicitud.

# 📌 Se define un enrutador para las rutas relacionadas con predicciones.
PREDICT_ROUTER = APIRouter()

""" @PREDICT_ROUTER.post("/predict/{model_name}", response_model=PredictionResponse)
async def predict_endpoint(model_name: str, request: PredictionRequest):
    try:
        result = predict(model_name, request)
        return {"model": model_name, "prediction": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}") """
    

# 🟢 Endpoint para realizar una predicción y guardarla en la base de datos.
@PREDICT_ROUTER.post("/predict/save/{model_name}/{user_id}", response_model=PredictionResponse)
async def predict_endpoint(model_name: str, 
                           user_id: str, 
                           request: PredictionRequest, 
                           db: Session = Depends(get_db)):
    """
    Realiza una predicción utilizando un modelo específico y guarda el resultado en la base de datos.

    - **model_name**: Nombre del modelo a utilizar.
    - **user_id**: ID del usuario que realiza la predicción.
    - **request**: Datos de entrada requeridos para la predicción.
    - **db**: Sesión de la base de datos inyectada.

    Retorna:
    - `model`: Nombre del modelo utilizado.
    - `prediction`: Información de la predicción almacenada en la base de datos.
    """
    try:
        # 🔄 Guarda la predicción en la base de datos
        prediction_db = save_prediction(user_id, request, db, model_name)

        # 📌 Retorna la respuesta con el modelo y la predicción guardada.
        return {
            "model": model_name,
            "prediction": prediction_db
        }
    
    except ValueError as e:
        # 🚨 Manejo de error cuando los datos de entrada no son válidos.
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # 🚨 Manejo de error interno del servidor.
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

