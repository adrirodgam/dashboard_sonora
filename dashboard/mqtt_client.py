import os
import time

import django
import paho.mqtt.client as mqtt
from django.utils import timezone

# ========= CONFIGURAR DJANGO =========
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
django.setup()

from django.core.cache import cache  # noqa: E402
from monitoreo.models import Municipio, Medicion  # noqa: E402


# ========= CONFIG MQTT =========
BROKER = "broker.emqx.io"
PUERTO = 1883
TOPIC = "sonora/#"  # Ejemplo: sonora/guaymas/temperatura


def on_connect(client, userdata, flags, rc):
    """
    Callback de conexión para paho-mqtt 1.x
    rc = 0  -> conexión exitosa
    """
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe(TOPIC)
        print(f"📡 Suscrito a: {TOPIC}")
    else:
        print("❌ Error de conexión MQTT. Código:", rc)


def on_message(client, userdata, msg):
    """Se ejecuta cada vez que llega un mensaje."""
    try:
        payload = msg.payload.decode("utf-8").strip()
        print(f"[MQTT] {msg.topic} -> {payload}")

        # Esperamos: sonora/<municipio>/<tipo>
        parts = msg.topic.split("/")
        if len(parts) < 3:
            return

        _, municipio_slug, tipo = parts[0], parts[1], parts[2]

        if tipo not in ("temperatura", "humedad", "luz"):
            # ignorar otros mensajes
            return

        valor = float(payload)

        municipio, _ = Municipio.objects.get_or_create(
            slug=municipio_slug,
            defaults={"nombre": municipio_slug.replace("_", " ").title()},
        )

        medicion = Medicion.objects.create(
            municipio=municipio,
            tipo=tipo,
            valor=valor,
            timestamp=timezone.now(),
        )

        # ======== ACTUALIZAR CACHE (para dashboard) ========
        cache_key = f"ultima_{municipio.slug}_{tipo}"
        cache_value = {
            "municipio": municipio.nombre,
            "slug": municipio.slug,
            "tipo": tipo,
            "valor": medicion.valor,
            "timestamp": medicion.timestamp.isoformat(),
        }
        cache.set(cache_key, cache_value, timeout=60 * 5)  # 5 minutos

    except ValueError:
        print("Payload no numérico, ignorado:", msg.payload)
    except Exception as e:
        print("Error procesando mensaje MQTT:", e)


def loop_mqtt():
    """
    Bucle principal de conexión con reconexión automática.
    Compatible con paho-mqtt 1.6.x
    """
    while True:
        try:
            client = mqtt.Client()  # <- sin CallbackAPIVersion
            client.on_connect = on_connect
            client.on_message = on_message

            print("Intentando conectar a MQTT...")
            client.connect(BROKER, PUERTO, keepalive=60)

            # loop_forever bloquea hasta que se pierda la conexión o haya error
            client.loop_forever()

        except Exception as e:
            print("MQTT desconectado:", e)
            print("Reintentando conexión en 5 segundos...")
            time.sleep(5)


if __name__ == "__main__":
    loop_mqtt()