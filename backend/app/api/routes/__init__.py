
# Importamos los routers de los diferentes módulos de la API
from .auth import AUTH_ROUTER  # Router para la autenticación de usuarios
from .predict import PREDICT_ROUTER  # Router para manejar predicciones de modelos
from .user import USER_ROUTER  # Router para gestionar operaciones sobre usuarios

# Definimos __all__ para controlar qué elementos son exportados cuando se importa este módulo
__all__ = ["AUTH_ROUTER", "PREDICT_ROUTER", "USER_ROUTER"]
# Solo se exportan los routers para su uso en otros módulos de la aplicación