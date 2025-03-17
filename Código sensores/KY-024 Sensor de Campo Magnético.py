import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = "linux4321"
MQTT_CLIENT_ID = "esp32_ky024"
MQTT_TOPIC = "campo_magnetico"
MQTT_PORT = 1883

SSID = "RaspBerry 7"
PASSWORD = "linux4321"

digital_pin = Pin(15, Pin.IN)

def detectar_campo():
    return "Campo magnético detectado" if digital_pin.value() == 1 else "No detecta campo magnético"

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.5)
    print(" Conectado!")

def conectar_mqtt():
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                                user=MQTT_USER, password=MQTT_PASSWORD, keepalive=30)
            client.connect()
            print(f"Conectado a BROKER")
            return client
        except OSError as e:
            print("Error en MQTT, reintentando en 5s:", e)
            sleep(5)

conectar_wifi()
client = conectar_mqtt()

while True:
    mensaje = detectar_campo()
    print(mensaje)

    try:
        client.publish(MQTT_TOPIC, mensaje)
    except OSError:
        print("Conexión MQTT perdida, reconectando...")
        client = conectar_mqtt()

    sleep(5)