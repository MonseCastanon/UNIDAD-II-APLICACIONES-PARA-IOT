import network
import time
import machine
from umqtt.simple import MQTTClient

# Configuración WiFi
SSID = "RaspBerry 7"
PASSWORD = "linux4321"

# Configuración del Broker MQTT (Mosquitto)
MQTT_BROKER = "192.168.137.164"
MQTT_CLIENT_ID = "ESP32_BUTTON"
MQTT_TOPIC_PUB = "push_button"
MQTT_PORT = 1883

# Opcional: Usuario y contraseña (si Mosquitto lo requiere)
MQTT_USER = "RaspBerry 7"
MQTT_PASSWORD = "linux4321"

# Configuración del botón (con pull-up interno)
button_pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

# Variables para el debounce
last_button_state = 1  # 1 porque el botón tiene pull-up (sin presionar)
last_debounce_time = 0
debounce_delay = 200  # 200 ms

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.5)

    print("\nConectado a WiFi:", sta_if.ifconfig())

# Función para conectar a MQTT
def conectar_mqtt():
    global client
    try:
        if MQTT_USER and MQTT_PASSWORD:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                                user=MQTT_USER, password=MQTT_PASSWORD)
        else:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        
        client.connect()
        print(f"Conectado a {MQTT_BROKER}")
    except Exception as e:
        print(f"Error de conexión MQTT: {e}")
        time.sleep(5)
        conectar_mqtt()  # Reintentar conexión

# Conectar a WiFi y MQTT
conectar_wifi()
conectar_mqtt()

# Bucle principal
while True:
    try:
        current_time = time.ticks_ms()
        button_state = button_pin.value()

        if button_state != last_button_state:  # Si cambia el estado del botón
            last_debounce_time = current_time  # Reinicia el tiempo de debounce

        if (current_time - last_debounce_time) > debounce_delay:  # Si pasó el debounce
            if button_state == 0:  # Se presionó el botón (LOW)
                print("Botón presionado, enviando MQTT...")
                client.publish(MQTT_TOPIC_PUB, "PRESIONADO")  # Publica el mensaje

        last_button_state = button_state  # Guarda el estado anterior
        time.sleep(0.1)  # Pequeña pausa para evitar consumo innecesario

    except Exception as e:
        print(f"Error: {e}")
        print("Intentando reconectar...")
        time.sleep(5)
        conectar_wifi()
        conectar_mqtt()