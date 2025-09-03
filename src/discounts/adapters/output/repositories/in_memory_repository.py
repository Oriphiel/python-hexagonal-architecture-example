# Este adaptador implementa la interfaz del puerto con una base de datos en memoria.
from typing import Optional, Dict, List
from src.discounts.domain.models import Discount
from src.discounts.application.ports.output.discount_repository import IDiscountRepository


class InMemoryDiscountRepository(IDiscountRepository):
    """Implementación de repositorio que guarda los datos en un diccionario."""

    def __init__(self):
        self._discounts: Dict[str, Discount] = {}
        print("ADAPTER (DB-IN-MEMORY): Repositorio en memoria inicializado.")

    def save(self, discount: Discount):
        print(f"ADAPTER (DB-IN-MEMORY): Guardando/Actualizando descuento '{discount.code}'...")
        self._discounts[discount.code] = discount

    def find_by_code(self, code: str) -> Optional[Discount]:
        print(f"ADAPTER (DB-IN-MEMORY): Buscando descuento '{code}'...")
        return self._discounts.get(code)

    def find_all(self) -> List[Discount]:
        print("ADAPTER (DB-IN-MEMORY): Devolviendo todos los descuentos...")
        return list(self._discounts.values())
