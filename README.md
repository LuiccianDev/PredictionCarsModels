# CarPredict - Sistema de Predicción de Precios de Autos

Sistema de predicción de precios de autos utilizando modelos de IA, construido con FastAPI y React.

## Estructura del Proyecto

```
PyPredictionCarModels/
├── backend/
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── init.sql
│   ├── routes/
│   │   ├── login.py
│   │   ├── prediction.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── prediction.py
│   │   └── user.py
│   ├── services/
│   │   └── prediction_service.py
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Footer.jsx
│   │   │   ├── Hero.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Prediction.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── models/
    └── utils/
        ├── load_model_prices_segmetation.py
        ├── load_model_prices_clusterization.py
        └── load_models_prices_prediction.py
```

## Requisitos

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

## Entrenamiento de Modelos

Los modelos de predicción de precios, segmentación y clusterización fueron entrenados utilizando datasets de autos con características como marca, modelo, año, kilometraje, entre otros. Se emplearon las siguientes técnicas:

- **Predicción de Precios**: Modelos de regresión como Random Forest y Gradient Boosting.
- **Segmentación**: Algoritmos de clasificación supervisada como SVM y Logistic Regression.
- **Clusterización**: Algoritmos no supervisados como K-Means y DBSCAN.

Los scripts de entrenamiento y preprocesamiento se encuentran en la carpeta `models/utils/`. Cada modelo se guarda en formato pickle para ser cargado dinámicamente en el backend.

## Backend

El backend está construido con **FastAPI** y proporciona una API REST para interactuar con los modelos y la base de datos. Principales características:

- **Estructura Modular**: Separación de responsabilidades en rutas, esquemas, servicios y configuración.
- **Base de Datos**: PostgreSQL para almacenar usuarios y predicciones.
- **Autenticación**: Sistema de login con JWT.
- **Endpoints**:
  - `POST /predict/`: Realiza predicciones de precios.
  - `POST /login/`: Autenticación de usuarios.
  - `GET /users/`: Lista de usuarios.
  - `POST /users/`: Crear nuevo usuario.

### Configuración del Backend

1. Crear un entorno virtual e instalar dependencias:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configurar variables de entorno en `.env`:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=root
   POSTGRES_DB=FastAPI_DB
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

3. Inicializar la base de datos ejecutando el script `init.sql`:
   ```bash
   psql -U postgres -d FastAPI_DB -f backend/database/init.sql
   ```

4. Iniciar el servidor:
   ```bash
   uvicorn main:app --reload
   ```

El backend estará disponible en [http://localhost:8000](http://localhost:8000).

## Frontend

El frontend está construido con **React** y utiliza **Vite** como herramienta de desarrollo. Principales características:

- **Diseño Moderno**: Interfaz responsive utilizando Tailwind CSS.
- **Componentes Reutilizables**: Navbar, Hero y Footer.
- **Páginas Principales**:
  - **Home**: Página de inicio con información general.
  - **Login**: Formulario de autenticación.
  - **Prediction**: Interfaz para realizar predicciones de precios.

### Configuración del Frontend

1. Instalar dependencias:
   ```bash
   cd frontend
   npm install
   ```

2. Iniciar el servidor de desarrollo:
   ```bash
   npm run dev
   ```

El frontend estará disponible en [http://localhost:3000](http://localhost:3000).

## Características

- **Predicción de Precios**: Utiliza modelos de IA para predecir precios de autos.
- **Segmentación**: Clasifica los autos en diferentes segmentos de mercado.
- **Clusterización**: Agrupa autos similares para mejor análisis.
- **Autenticación**: Sistema de login para usuarios.
- **Interfaz Moderna**: Diseño responsive con Tailwind CSS.

## API Endpoints

- `POST /predict/`: Realiza predicciones de precios.
- `POST /login/`: Autenticación de usuarios.
- `GET /users/`: Lista de usuarios.
- `POST /users/`: Crear nuevo usuario.

## Base de Datos

La aplicación utiliza PostgreSQL con dos tablas principales:
- `users`: Almacena información de usuarios.
- `predictions`: Almacena el historial de predicciones.

## Contribuir

1. Fork el repositorio.
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`).
4. Push a la rama (`git push origin feature/nueva-caracteristica`).
5. Crea un Pull Request.
