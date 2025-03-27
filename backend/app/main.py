from fastapi import FastAPI
from app.api import routes
from fastapi.middleware.cors import CORSMiddleware
from app.core import init_db 
from contextlib import asynccontextmanager  # ✅ Import necesario para lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("La aplicación se ha iniciado.")  # ✅ Reemplazo de @app.on_event("startup")
    yield  # Permite que la API corra normalmente
    print("La aplicación se está apagando.")  # ✅ Reemplazo de @app.on_event("shutdown")


app = FastAPI(
    title="Mi API",
    version="1.0.0",
    description="API para gestionar usuarios, predicciones y autenticación.",
    lifespan=lifespan  # ✅ Nuevo argumento que maneja el ciclo de vida
)

# Configurar CORS
origins = [
    "http://localhost:5173",  # URL del frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.USER_ROUTER, prefix="/api", tags=["users"])
app.include_router(routes.PREDICT_ROUTER, prefix="/api", tags=["predictions"])
app.include_router(routes.AUTH_ROUTER, prefix="/api", tags=["auth"])


init_db()
# Endpoint raíz para comprobar el estado de la API
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", port=8888, reload=True)

