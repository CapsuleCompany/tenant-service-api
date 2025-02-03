from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tenant
import requests
from django.conf import settings
from kafka import KafkaProducer
import json

USER_API_URL = settings.USER_SERVICE_API + "users/tenant/"
KAFKA_TOPIC = settings.KAFKA_TOPIC
KAFKA_SERVERS = settings.KAFKA_SERVERS

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)


@receiver(post_save, sender=Tenant)
def associate_user_with_tenant(sender, instance, created, **kwargs):
    if created:
        try:
            response = requests.post(
                USER_API_URL,
                json={"tenant_id": str(instance.id), "user": str(instance.user_id)},
                timeout=10,
            )

            match response.status_code:
                case 201:
                    print("Tenant associated successfully.")
                case 400:
                    # Send the event to Kafka in case of client-side error
                    producer.send(
                        KAFKA_TOPIC,
                        {
                            "event": "tenant_association_failed",
                            "tenant_id": str(instance.id),
                            "user_id": str(instance.user_id),
                            "reason": "Bad Request (400)",
                        },
                    )
                    print("Tenant association failed - sent to Kafka: Bad Request (400)")
                case 500:
                    # Send the event to Kafka in case of server-side error
                    producer.send(
                        KAFKA_TOPIC,
                        {
                            "event": "tenant_association_failed",
                            "tenant_id": str(instance.id),
                            "user_id": str(instance.user_id),
                            "reason": "Server Error (500)",
                        },
                    )
                    print("Tenant association failed - sent to Kafka: Server Error (500)")
                case _:
                    # Handle other status codes
                    producer.send(
                        KAFKA_TOPIC,
                        {
                            "event": "tenant_association_failed",
                            "tenant_id": str(instance.id),
                            "user_id": str(instance.user_id),
                            "reason": f"Unexpected status code: {response.status_code}",
                        },
                    )
                    print(
                        f"Tenant association failed - sent to Kafka: Unexpected status code {response.status_code}"
                    )

        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
        except requests.ConnectionError:
            print("Failed to connect to the user API.")
        except requests.Timeout:
            print("Request timed out.")
        except requests.RequestException as e:
            print(f"Error reaching the user API: {e}")
            # Send error details to Kafka
            producer.send(
                KAFKA_TOPIC,
                {
                    "event": "tenant_association_failed",
                    "tenant_id": str(instance.id),
                    "user_id": str(instance.user_id),
                    "reason": str(e),
                },
            )
            print("Error details sent to Kafka.")