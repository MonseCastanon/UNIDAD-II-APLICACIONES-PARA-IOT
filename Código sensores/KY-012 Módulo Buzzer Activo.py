import network
import time
import machine
from umqtt.simple import MQTTClient

# Configuración de la red WiFi
SSID = "RaspBerry 7"
PASSWORD = "linux4321"

# Configuración del broker MQTT
MQTT_BROKER = "192.168.137.164"  # IP del broker en la Raspberry Pi
MQTT_PORT = 1883  # Puerto estándar MQTT
MQTT_TOPIC = "ky10_sensor"

# Configuración del pin donde está conectado el buzzer (pin digital)
buzzer_pin = machine.Pin(5, machine.Pin.OUT)

# Conectar a WiFi
def connect_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print("\nWiFi Conectada!")

# Conectar al broker MQTT con reintentos
def connect_mqtt():
    client = MQTTClient("photo_client", MQTT_BROKER, port=MQTT_PORT)
    retries = 5
    while retries > 0:
        try:
            print("Intentando conectar al broker MQTT...")
            client.connect()
            print("Conectado al broker MQTT")
            return client
        except OSError as e:
            print(f"Error de conexión al MQTT: {e}")
            retries -= 1
            time.sleep(5)  # Esperar antes de reintentar
    print("No se pudo conectar al broker MQTT después de varios intentos.")
    machine.reset()  # Reiniciar si no se conecta

# Publicar datos del sensor
def publish_data():
    client = connect_mqtt()
    while True:
        # Encender el buzzer
        buzzer_pin.value(1)
        print("Buzzer encendido")
        # Publicar estado del buzzer en MQTT
        client.publish(MQTT_TOPIC, "Buzzer encendido")
        time.sleep(1)

        # Apagar el buzzer
        buzzer_pin.value(0)
        print("Buzzer apagado")
        # Publicar estado del buzzer en MQTT
        client.publish(MQTT_TOPIC, "Buzzer apagado")
        time.sleep(1)

# Conectar a WiFi
connect_wifi()

# Publicar los datos del sensor
publish_data()  # Esta función ahora publicará constantemente los datos del sensor