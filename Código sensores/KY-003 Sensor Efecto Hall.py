import machine
import time
import network
from umqtt.simple import MQTTClient

SENSOR_PIN = 15 
sensor = machine.Pin(SENSOR_PIN, machine.Pin.IN)

WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor_hall"

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

conectar_wifi()

client = MQTTClient("ESP32", MQTT_BROKER, port=MQTT_PORT, keepalive=60)
client.connect()

try:
    while True:
        estado = sensor.value()
        if estado == 0:
            mensaje = "¡Campo magnético detectado!"
        else:
            mensaje = "No hay campo magnético"
        
        print(mensaje)  
        client.publish(MQTT_TOPIC, mensaje.encode())  
        
        time.sleep(1) 

except KeyboardInterrupt:
    print("Programa detenido")
    client.disconnect() 