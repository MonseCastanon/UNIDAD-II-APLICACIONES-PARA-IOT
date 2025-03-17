import network
import time
import machine
from umqtt.simple import MQTTClient

WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor_linea"
MQTT_CLIENT_ID = "ESP32_LINEA_SENSOR"

# Configuración del sensor KY-033
SENSOR_PIN = 4  
sensor = machine.Pin(SENSOR_PIN, machine.Pin.IN)

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    timeout = 10  
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
    
    if wlan.isconnected():
        print("Conectado a WiFi:", wlan.ifconfig())
    else:
        print("No se pudo conectar a WiFi")
        machine.reset()

def conectar_mqtt():
    global client
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=30)
            client.connect()
            print(f"Conectado a MQTT en {MQTT_BROKER}")
            return
        except OSError as e:
            print("Error conectando a MQTT, reintentando en 5 segundos:", e)
            time.sleep(5)

conectar_wifi()
conectar_mqtt()

try:
    while True:
        estado = sensor.value()  
        
        if estado == 0:
            print("Línea detectada (Negro)")
            client.publish(MQTT_TOPIC, "NEGRO")
        else:
            print("No hay línea (Blanco)")
            client.publish(MQTT_TOPIC, "BLANCO")
        
        time.sleep(3) 

except KeyboardInterrupt:
    print("Programa detenido")
    client.disconnect()