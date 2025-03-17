import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración de la red WiFi
SSID = "RaspBerry 7"
PASSWORD = "linux4321"

# Configuración del broker MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_sound_sensor"
MQTT_DIGITAL_TOPIC = "soundS_sensor"
MQTT_ANALOG_TOPIC = "soundS_sensor"

# Configuración del sensor de sonido
SOUND_DIGITAL_PIN = 35  # Salida Digital (DO)
SOUND_ANALOG_PIN = 34  # Salida Analógica (AO)

sound_digital = Pin(SOUND_DIGITAL_PIN, Pin.IN)  # Entrada digital
sound_analog = ADC(Pin(SOUND_ANALOG_PIN))  # Entrada analógica
sound_analog.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V

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
        digital_status = sound_digital.value()  # 1 = Sonido detectado, 0 = Silencio
        analog_value = sound_analog.read()  # Valor entre 0 y 4095

        estado = "SONIDO DETECTADO" if digital_status == 1 else "SILENCIO"
        
        print(f"Estado Digital: {estado}, Nivel Analógico: {analog_value}")
        
        client.publish(MQTT_DIGITAL_TOPIC, estado)
        client.publish(MQTT_ANALOG_TOPIC, str(analog_value))
        
        sleep(1)  # Publica cada 1 segundo

# Iniciar el programa
conectar_wifi()
publicar_datos()