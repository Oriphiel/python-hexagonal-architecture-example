# Este archivo es el único que conoce las implementaciones concretas.
# Aquí se realiza la Inyección de Dependencias.
from fastapi import FastAPI
from src.discounts.adapters.output.event_publishers.log_publisher import LogEventPublisher
from src.discounts.adapters.output.repositories.in_memory_repository import InMemoryDiscountRepository
from src.discounts.application.services import DiscountService
from src.discounts.adapters.output.repositories.sqlite_repository import SqliteDiscountRepository

# -- Inyección de Dependencias (El Corazón de la Arquitectura) --
print("COMPOSITION ROOT: Configurando la aplicación...")

DB_FILE = "discounts.db"

# 1. Crear instancias de los adaptadores de salida (infraestructura)
# discount_repository = InMemoryDiscountRepository() # In memory
discount_repository = SqliteDiscountRepository(db_path=DB_FILE) # Database
event_publisher = LogEventPublisher()

# 2. Crear instancia del servicio del núcleo, inyectando los adaptadores como dependencias
discount_service = DiscountService(
    repository=discount_repository,
    event_publisher=event_publisher
)

# 3. Función que los adaptadores de entrada usarán para obtener el servicio ya configurado
def get_discount_service():
    return discount_service
# -- Fin de la Inyección --


# Crear la aplicación API de FastAPI
app = FastAPI(
    title="Sistema de Descuentos Hexagonal",
    description="Ejemplo de Arquitectura Hexagonal con FastAPI y Python",
    version="1.0.0"
)
from src.discounts.adapters.input.api.router import router as api_router
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok"}

print("COMPOSITION ROOT: Configuración completada. La aplicación está lista.")
