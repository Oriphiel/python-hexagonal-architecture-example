# Define lo que el núcleo NECESITA hacer con la persistencia.
import abc
from typing import Optional, List
from src.discounts.domain.models import Discount


class IDiscountRepository(abc.ABC):
    """Interfaz (Puerto) para el repositorio de descuentos."""

    @abc.abstractmethod
    def save(self, discount: Discount):
        """Guarda un descuento en la persistencia."""
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_code(self, code: str) -> Optional[Discount]:
        """Busca un descuento por su código."""
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self) -> List[Discount]:
        """Devuelve todos los descuentos existentes."""
        raise NotImplementedError
