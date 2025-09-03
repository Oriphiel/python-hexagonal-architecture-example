# Importa los puertos (interfaces), no las implementaciones concretas.
from typing import List, Optional
from src.discounts.domain.models import Discount, Cart, DomainEvent
from src.discounts.application.ports.output.discount_repository import IDiscountRepository
from src.discounts.application.ports.output.event_publisher import IEventPublisher


class DiscountService:
    """
    Este es el caso de uso principal. Orquesta la lógica del dominio
    y se comunica con el exterior a través de los puertos.
    """

    def __init__(
            self,
            repository: IDiscountRepository,
            event_publisher: IEventPublisher
    ):
        self.repository = repository
        self.event_publisher = event_publisher

    def create_discount(self, code: str, percentage: float) -> Discount:
        """Caso de uso para crear un descuento."""
        print(f"\n--- Caso de Uso: Creando descuento '{code}' ---")
        # Aquí podrían ir validaciones de negocio complejas
        if percentage > 50:
            raise ValueError("Regla de Negocio: No se permiten descuentos superiores al 50%.")
        if self.repository.find_by_code(code):
            raise ValueError(f"Regla de Negocio: El código de descuento '{code}' ya existe.")

        new_discount = Discount(code=code, percentage=percentage)
        self.repository.save(new_discount)
        print(f"SERVICE: Descuento '{code}' creado y delegado al repositorio para guardar.")
        return new_discount

    def request_discount_validation(self, code: str, cart: Cart):
        """
        Caso de uso para solicitar una validación. No la ejecuta,
        sino que publica un evento para que se procese de forma asíncrona.
        """
        print(f"\n--- Caso de Uso: Solicitando validación para '{code}' ---")
        discount = self.repository.find_by_code(code)

        if not discount or not discount.is_active:
            print(f"SERVICE: Descuento '{code}' no válido o no encontrado. No se publica evento.")
            # En un caso real, podríamos publicar un evento de "fallo"
            return

        # Creamos un evento de dominio con la información necesaria
        validation_event = DomainEvent(
            event_name="DiscountValidationRequested",
            payload={
                "discount_code": code,
                "cart_id": cart.cart_id,
                "user_id": cart.user_id,
                "cart_total": cart.total_amount,
            }
        )

        # Usamos el puerto para publicar el evento
        self.event_publisher.publish(validation_event)
        print(f"SERVICE: Evento de validación para '{code}' publicado para procesamiento asíncrono.")

    def get_all_discounts(self) -> List[Discount]:
        """Caso de uso para obtener todos los descuentos."""
        print("\n--- Caso de Uso: Obteniendo todos los descuentos ---")
        return self.repository.find_all()

    def get_discount_by_code(self, code: str) -> Optional[Discount]:
        """Caso de uso para obtener un descuento específico por su código."""
        print(f"\n--- Caso de Uso: Obteniendo descuento '{code}' ---")
        return self.repository.find_by_code(code)
