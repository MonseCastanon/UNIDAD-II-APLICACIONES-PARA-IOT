from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_client"
MQTT_SENSOR_TOPIC = "modulo_encoder"
MQTT_PORT = 1883

# Configuración del sensor KY-040
clk = Pin(32, Pin.IN, Pin.PULL_UP)
dt = Pin(33, Pin.IN, Pin.PULL_UP)
button = Pin(25, Pin.IN, Pin.PULL_UP)

last_state = clk.value()


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
        current_state = clk.value()
        
        if current_state != last_state:
            if dt.value() != current_state:
                mensaje = "Sentido horario"
            else:
                mensaje = "Sentido antihorario"
            
            client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())
            print(f"[INFO] Publicado en {MQTT_SENSOR_TOPIC}: {mensaje}")
        
        last_state = current_state
        
        if not button.value():
            mensaje = "Botón presionado"
            client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())
            print(f"[INFO] Publicado en {MQTT_SENSOR_TOPIC}: {mensaje}")
            time.sleep(0.5)
        
        time.sleep(0.1)
    
    except Exception as e:
        print(f"[ERROR] Error en el loop principal: {e}")
        client = None
