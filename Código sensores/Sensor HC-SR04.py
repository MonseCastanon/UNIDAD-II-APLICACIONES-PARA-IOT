from machine import Pin, time_pulse_us
import time
import network
from umqtt.simple import MQTTClient

MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_client"
MQTT_SENSOR_TOPIC = "sensor_distancia"
MQTT_PORT = 1883

# Configuración del sensor HC-SR04
TRIGGER_PIN = 32
ECHO_PIN = 33

trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

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

def medir_distancia():
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    tiempo = time_pulse_us(echo, 1, 30000)
    if tiempo < 0:
        return None

    distancia = (tiempo * 0.0343) / 2
    return round(distancia, 2)

conectar_wifi()
client = subscribir()

while True:
    try:
        distancia = medir_distancia()
        if distancia is not None:
            mensaje = f"Distancia: {distancia} cm"
            client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())
            print(f"[INFO] Publicado en {MQTT_SENSOR_TOPIC}: {mensaje}")
        else:
            print("[WARN] Error en la medición")
        
        time.sleep(3)

    except Exception as e:
        print(f"[ERROR] Error en el loop principal: {e}")
        client = None