import json
from pathlib import Path
from ModelTrain.utils.logger import logger

# Definir la ruta del archivo JSON para datos desconocidos
PATH_JSON_ERROR_DATA = Path(__file__).resolve().parent.parent.parent / "data" / "unseen_data"
PATH_JSON_ERROR_DATA.mkdir(parents=True, exist_ok=True)

def save_unseen_data(car_data, names: str = "unseen_data.json"):
    """
    Guarda los datos no vistos en un archivo JSON sin duplicados.

    Parámetros:
        car_data (dict): Diccionario con los datos del auto que no se pudieron predecir.
        names (str): Nombre del archivo JSON donde se guardarán los datos.

    Retorna:
        bool: True si se guardó exitosamente, False en caso de error.
    """
    file_path = PATH_JSON_ERROR_DATA / names
    try:
        # Cargar datos previos si el archivo existe
        if file_path.exists():
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    unseen_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.warning(f"Error al cargar JSON, iniciando con lista vacía: {e}")
                unseen_data = []
        else:
            unseen_data = []

        # Convertir los datos actuales en un conjunto para evitar duplicados
        unseen_data_set = {json.dumps(item, sort_keys=True) for item in unseen_data}

        # Convertir el nuevo dato a JSON y verificar si ya existe
        new_data_json = json.dumps(car_data, sort_keys=True)
        if new_data_json not in unseen_data_set:
            unseen_data.append(car_data)

            # Guardar datos en el archivo JSON
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(unseen_data, f, indent=4, ensure_ascii=False)

            logger.info(f"Datos desconocidos guardados en {file_path}")
        else:
            logger.info(f"Datos ya existentes, no se guardarán duplicados.")

        return True
    except Exception as e:
        logger.error(f"Error al guardar datos no vistos: {e}", exc_info=True)
        return False

def save_prices_prediction(car_data):
    save_unseen_data(car_data, names="unseen_data_price.json")

def save_prices_segmentation(car_data):
    save_unseen_data(car_data, names="unseen_data_segmentation.json")

def save_prices_clusterization(car_data):
    save_unseen_data(car_data, names="unseen_data_clusterization.json")
