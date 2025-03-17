from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración del broker MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "sensor_flama"
MQTT_PORT = 1883

pin_analogico = ADC(Pin(34))
pin_analogico.atten(ADC.ATTN_11DB)

pin_digital = Pin(32, Pin.IN)


def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('RaspBerry 7', 'linux4321')  
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
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
    valor_analogico = pin_analogico.read()
    valor_digital = pin_digital.value() 

    if valor_analogico == 0:
        print("Flama detectada")
        client.publish(MQTT_SENSOR_TOPIC, ("Flama detectada").encode())
    else:
        print("Sin flama")
        client.publish(MQTT_SENSOR_TOPIC, ("Sin flama").encode())

    time.sleep(4) 