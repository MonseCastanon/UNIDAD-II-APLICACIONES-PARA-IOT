import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración de la red WiFi
SSID = "RaspBerry 7"
PASSWORD = "linux4321"

# Configuración del broker MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_water_sensor"
MQTT_TOPIC = "water_sensor"

# Configuración del sensor de agua (Salida Digital)
WATER_SENSOR_PIN = 35 
water_sensor = Pin(WATER_SENSOR_PIN, Pin.IN)

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.5)
    print("\nWiFi Conectada!")

# Función para conectar a MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    try:
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print(f"Error de conexión al MQTT: {e}")
        return None

# Función principal para publicar datos
def publicar_datos():
    client = conectar_mqtt()
    if client is None:
        return
    
    while True:
        water_status = water_sensor.value()  # 1 = Agua detectada, 0 = No hay agua
        estado = "AGUA DETECTADA" if water_status == 1 else "SIN AGUA"
        
        print(f"Estado del agua: {estado}")
        client.publish(MQTT_TOPIC, estado)
        
        sleep(5)  # Publica cada 5 segundos

# Iniciar el programa
conectar_wifi()
publicar_datos()