import machine
import time
import network
from umqtt.simple import MQTTClient

SENSOR_PIN = 34
sensor = machine.ADC(machine.Pin(SENSOR_PIN))
sensor.atten(machine.ADC.ATTN_11DB)

WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_TOPIC = "sensol_hall_analogico"
MQTT_CLIENT_ID = "ESP32_HALL"

UMBRAL_SUPERIOR = 2.0
UMBRAL_INFERIOR = 1.3

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
        raw_value = sensor.read()  
        voltage = (raw_value / 4095.0) * 3.3  

        if voltage >= UMBRAL_SUPERIOR or voltage <= UMBRAL_INFERIOR:
            mensaje = "¡Campo magnético detectado!"
        else:
            mensaje = "No hay campo magnético"

        print(mensaje)

        try:
            client.publish(MQTT_TOPIC, mensaje.encode())
        except OSError:
            print("Conexión MQTT perdida, reconectando...")
            conectar_mqtt()

        time.sleep(5)

except KeyboardInterrupt:
    print("Programa detenido")
    client.disconnect()