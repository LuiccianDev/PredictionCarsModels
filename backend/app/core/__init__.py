from app.core.config import settings  
# Importa la configuración de la aplicación, que contiene las variables de entorno y los parámetros de configuración.

from app.core.database import get_db, init_db  
# Importa:
# - `get_db`: Función generadora que proporciona una sesión de base de datos para cada solicitud.
# - `init_db`: Función que inicializa la base de datos creando las tablas definidas en los modelos.

# Se define `__all__` para especificar qué elementos se pueden importar desde este módulo.
# Solo se exportan `settings`, `get_db` e `init_db` para su uso en otros módulos de la aplicación.
__all__ = ["settings", "get_db", "init_db"]


""" 🔥 Beneficios de __all__
✅ Control de exportaciones: Solo settings será accesible si alguien hace from app.core import *.
✅ Evita importar cosas innecesarias: No se importará todo lo que esté en config.py.
✅ Código más limpio: Puedes hacer from app.core import settings en lugar de from app.core.config import settings. """