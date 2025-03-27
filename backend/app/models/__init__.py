from .users_models import User  
# Importa el modelo de la tabla `users`, que representa a los usuarios en la base de datos.

from .predictions_models import Prediction  
# Importa el modelo de la tabla `predictions`, que almacena las predicciones realizadas por los usuarios.

from .result_prediction_models import PricesCluster, PricesSegmentation, PricesPrediction  
# Importa los modelos de las tablas:
# - `PricesCluster`: Resultados del modelo de clusterización (KMeans y DBSCAN).
# - `PricesSegmentation`: Resultados del modelo de segmentación (RF, SVM, MLP).
# - `PricesPrediction`: Resultados del modelo de predicción de precios (RF, XGB, DNN).

# Se define una lista con todos los modelos disponibles en la base de datos.
# Esto permite que SQLAlchemy registre automáticamente estos modelos al inicializar la aplicación.
__all__ = ["User", "Prediction", "PricesCluster", "PricesSegmentation", "PricesPrediction"]
