from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tenant.models import Tenant, TenantPlan
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
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# @receiver(post_save, sender=Tenant)
# def create_tenant_plan(sender, instance, created, **kwargs):
#     if created:
#         TenantPlan.objects.create(tenant_id=instance.id)


@receiver(post_save, sender=Tenant)
def associate_user_with_tenant(sender, instance, created, **kwargs):
    if created:
        try:
            response = requests.post(
                USER_API_URL,
                json={"tenant_id": str(instance.id), "user": str(instance.owner_id)},
                timeout=10,
            )

            match response.status_code:
                case 201:
                    print("Tenant associated successfully.")
                case 400:
                    producer.send(
                        KAFKA_TOPIC,
                        {
                            "event": "tenant_association_failed",
                            "tenant_id": str(instance.id),
                            "user_id": str(instance.user_id),
                            "reason": "Bad Request (400)",
                        },
                    )
                    print(
                        "Tenant association failed - sent to Kafka: Bad Request (400)"
                    )
                case 500:
                    producer.send(
                        KAFKA_TOPIC,
                        {
                            "event": "tenant_association_failed",
                            "tenant_id": str(instance.id),
                            "user_id": str(instance.user_id),
                            "reason": "Server Error (500)",
                        },
                    )
                    print(
                        "Tenant association failed - sent to Kafka: Server Error (500)"
                    )
                case _:
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

        except requests.RequestException as e:
            print(f"Error reaching the user API: {e}")
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


@receiver(post_delete, sender=Tenant)
def remove_user_association(sender, instance, **kwargs):
    """
    When a Tenant is deleted, notify the User Service and Kafka.
    """
    try:
        response = requests.delete(
            f"{USER_API_URL}{instance.id}/",
            timeout=10,
        )

        match response.status_code:
            case 200:
                print("Tenant association removed successfully.")
            case 404:
                print("Tenant association not found in user service.")
            case 400 | 500:
                producer.send(
                    KAFKA_TOPIC,
                    {
                        "event": "tenant_deletion_failed",
                        "tenant_id": str(instance.id),
                        "user_id": str(instance.user_id),
                        "reason": f"Failed with status {response.status_code}",
                    },
                )
                print(
                    f"Tenant deletion failed - sent to Kafka: Status {response.status_code}"
                )
            case _:
                producer.send(
                    KAFKA_TOPIC,
                    {
                        "event": "tenant_deletion_failed",
                        "tenant_id": str(instance.id),
                        "user_id": str(instance.user_id),
                        "reason": f"Unexpected status code: {response.status_code}",
                    },
                )
                print(
                    f"Unexpected response code {response.status_code} for tenant deletion."
                )

    except requests.RequestException as e:
        print(f"Error removing tenant association: {e}")
        producer.send(
            KAFKA_TOPIC,
            {
                "event": "tenant_deletion_failed",
                "tenant_id": str(instance.id),
                "user_id": str(instance.user_id),
                "reason": str(e),
            },
        )
        print("Error details sent to Kafka.")
