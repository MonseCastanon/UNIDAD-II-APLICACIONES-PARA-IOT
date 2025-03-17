import machine
import time
import network
from umqtt.simple import MQTTClient

# CONFIGURACIÓN DEL SENSOR KY-021
SENSOR_PIN = 15  # Cambia este pin si lo conectas a otro GPIO
sensor = machine.Pin(SENSOR_PIN, machine.Pin.IN)

WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor_magnetico"

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

# CONECTAR A WIFI
conectar_wifi()

# CONFIGURAR CLIENTE MQTT
client = MQTTClient("ESP32", MQTT_BROKER, port=MQTT_PORT, keepalive=60)
client.connect()

# BUCLE PRINCIPAL
try:
    while True:
        estado = sensor.value()
        if estado == 0:
            mensaje = "¡Imán detectado!"
        else:
            mensaje = "No hay imán"
        
        print(mensaje)  # Muestra el estado en la consola
        client.publish(MQTT_TOPIC, mensaje.encode())  # Enviar a MQTT
        
        time.sleep(1)  # Pequeño retardo para evitar lecturas continuas

except KeyboardInterrupt:
    print("Programa detenido")
    client.disconnect()