# No hay importaciones de frameworks o bases de datos aquí. ¡Puro Python!
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Discount:
    """Representa un descuento en nuestro sistema. Es una entidad pura."""
    code: str
    percentage: float
    is_active: bool = True

    def deactivate(self):
        """Regla de negocio: Un descuento se puede desactivar."""
        if not self.is_active:
            # Podríamos lanzar una excepción de dominio aquí
            print(f"WARN: El descuento '{self.code}' ya estaba inactivo.")
        self.is_active = False

@dataclass
class Cart:
    """Representa un carrito de compras simple."""
    cart_id: str
    total_amount: float
    user_id: str

@dataclass
class DomainEvent:
    """Clase base para eventos de dominio."""
    event_name: str
    payload: Dict[str, Any]
