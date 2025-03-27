def validate_car_data(car_data):
    """
    Valida que los datos del auto tengan todas las claves requeridas y sean del tipo correcto.
    
    Parámetros:
        car_data (dict): Diccionario con los datos de un auto.
    
    Retorna:
        dict: Diccionario validado si es correcto.
    
    Lanza:
        ValueError: Si falta algún campo o tiene un tipo de dato incorrecto.
    """
    required_keys = {
        "Brand": str,
        "Model": str,
        "Year": int,
        "Engine_Size": float,
        "Fuel_Type": str,
        "Transmission": str,
        "Mileage": int,
        "Doors": int,
        "Owner_Count": int
    }

    for key, expected_type in required_keys.items():
        if key not in car_data:
            raise ValueError(f"❌ Falta el campo obligatorio: {key}")

        if not isinstance(car_data[key], expected_type):
            raise ValueError(f"❌ El campo '{key}' debe ser de tipo {expected_type.__name__}, pero recibió {type(car_data[key]).__name__}")

    return car_data
