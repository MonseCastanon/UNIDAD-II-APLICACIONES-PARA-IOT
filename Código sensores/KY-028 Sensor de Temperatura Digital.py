import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = "linux4321"
MQTT_CLIENT_ID = "esp32_temp"
MQTT_TEMP_TOPIC = "ky28_sensor"
MQTT_DIGITAL_TOPIC = "ky28_sensor"
MQTT_PORT = 1883

# Configuración de la red WiFi
SSID = "RaspBerry 7"
PASSWORD = "linux4321"

# Configuración del sensor KY-028
analog_temp = ADC(Pin(34))  # Pin de salida analógica
analog_temp.atten(ADC.ATTN_11DB)  # Rango completo de 0 a 3.3V
digital_temp = Pin(35, Pin.IN)  # Pin de salida digital

def get_temperature():
    raw_value = analog_temp.read()
    temperature = (raw_value / 4095.0) * 100  # Conversión aproximada
    return round(temperature, 2)

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('RaspBerry 7', 'linux1234')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" Conectado!")

def subscribir():
    global client
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    return client

# Conectar a WiFi
conectar_wifi()
# Subscripción a MQTT
client = subscribir()

# Ciclo de lectura de temperatura
while True:
    temperature = get_temperature()
    digital_status = digital_temp.value()
    print(f"Temperatura: {temperature}°C, Estado Digital: {digital_status}")
    client.publish(MQTT_TEMP_TOPIC, str(temperature))
    client.publish(MQTT_DIGITAL_TOPIC, "NORMAL" if digital_status == 1 else "ALERTA")
    sleep(5)