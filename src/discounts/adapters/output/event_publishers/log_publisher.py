# Este adaptador implementa el publicador de eventos simplemente escribiendo en la consola.
from src.discounts.domain.models import DomainEvent
from src.discounts.application.ports.output.event_publisher import IEventPublisher

class LogEventPublisher(IEventPublisher):
    """
    Implementación del publicador de eventos que imprime el evento en la consola.
    Simula enviarlo a un sistema de colas como Pub/Sub o RabbitMQ.
    """
    def __init__(self):
        print("ADAPTER (PUBSUB-LOG): Publicador de eventos en Log inicializado.")

    def publish(self, event: DomainEvent):
        print("--------------------------------------------------")
        print(f"ADAPTER (PUBSUB-LOG): Publicando evento '{event.event_name}'...")
        print("Payload del evento:")
        for key, value in event.payload.items():
            print(f"  - {key}: {value}")
        print("--------------------------------------------------")
        # En un caso real, aquí iría el código para enviar a la cola:
        # self.pubsub_client.publish(topic, event.to_json())
