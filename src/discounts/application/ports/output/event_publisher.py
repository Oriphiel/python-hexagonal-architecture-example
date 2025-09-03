# Define lo que el núcleo NECESITA hacer para notificar al mundo exterior.
import abc
from src.discounts.domain.models import DomainEvent

class IEventPublisher(abc.ABC):
    """Interfaz (Puerto) para un publicador de eventos de dominio."""

    @abc.abstractmethod
    def publish(self, event: DomainEvent):
        """Publica un evento de dominio."""
        raise NotImplementedError
