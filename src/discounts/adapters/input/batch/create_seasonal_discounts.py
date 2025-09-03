# Este es un adaptador para un proceso que se ejecuta manualmente o con un cron.
import sys
import os

# Esto es un truco para poder importar desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from main import get_discount_service


def run_batch_job():
    """Simula un proceso batch que crea descuentos de temporada."""
    print("==============================================")
    print("ADAPTER (BATCH): Iniciando proceso batch...")
    discount_service = get_discount_service()

    seasonal_discounts = {
        "VERANO25": 25.0,
        "INVIERNO15": 15.0,
    }

    for code, percentage in seasonal_discounts.items():
        try:
            discount_service.create_discount(code=code, percentage=percentage)
        except ValueError as e:
            print(f"ADAPTER (BATCH): No se pudo crear el descuento '{code}'. Razón: {e}")

    print("ADAPTER (BATCH): Proceso batch finalizado.")
    print("==============================================")


if __name__ == "__main__":
    run_batch_job()
