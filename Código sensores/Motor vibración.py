from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_client"
MQTT_SENSOR_TOPIC = "vibracion_motor"
MQTT_PORT = 1883

# Configuración del motor de vibración
motor = Pin(26, Pin.OUT)


def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('RaspBerry 7', 'linux4321') 
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)  
    print(" ¡Conectado!")


def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Suscrito al tópico {MQTT_SENSOR_TOPIC}")
    return client

conectar_wifi()

client = subscribir()

while True:
    try:
        motor.value(1)
        mensaje = "Motor activado"
        client.publish(MQTT_SENSOR_TOPIC, mensaje.encode()) 
        print(f"[INFO] Publicado en {MQTT_SENSOR_TOPIC}: {mensaje}")

        time.sleep(3)

        motor.value(0)
        mensaje = "Motor desactivado"
        client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())
        print(f"[INFO] Publicado en {MQTT_SENSOR_TOPIC}: {mensaje}")

        time.sleep(3) 

    except Exception as e:
        print(f"[ERROR] Error en el loop principal: {e}")
        client = None 