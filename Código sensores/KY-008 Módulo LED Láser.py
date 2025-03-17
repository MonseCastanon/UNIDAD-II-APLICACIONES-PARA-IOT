import network
import time
import machine
from umqtt.simple import MQTTClient

# Configuración WiFi
SSID = "RaspBerry 7"  # Cambia esto por tu red WiFi
PASSWORD = "linux4321"  # Contraseña de tu red WiFi

# Configuración Broker MQTT (Mosquitto)
MQTT_BROKER = "192.168.137.164"  # Dirección IP del Broker MQTT
MQTT_CLIENT_ID = "ESP32_LASER"  # ID único para tu cliente MQTT
MQTT_TOPIC_SUB = "led_laser"  # Tema de suscripción
MQTT_TOPIC_PUB = "led_laser"  # Tema para publicar estado del LED
MQTT_PORT = 1883  # Puerto MQTT (por defecto 1883)

# Configuración del pin para el LED Láser (Asegúrate de que el pin sea el correcto)
laser_pin = machine.Pin(5, machine.Pin.OUT)  # GPIO 5 para LED

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(10)

    print("\n Conectado a WiFi:", sta_if.ifconfig())

# Callback para recibir los mensajes MQTT
def callback(topic, msg):
    mensaje = msg.decode("utf-8")
    print(f"Mensaje recibido: {mensaje}")

    if mensaje == "ON":
        laser_pin.on()  # Encender el LED Láser
        print("Láser ENCENDIDO")
    elif mensaje == "OFF":
        laser_pin.off()  # Apagar el LED Láser
        print("Láser APAGADO")
    else:
        print(f"Mensaje desconocido: {mensaje}")

# Función para publicar el estado del LED
def publicar_estado(estado):
    try:
        client.publish(MQTT_TOPIC_PUB, estado)  # Publica el estado (ON/OFF)
        print(f"Estado enviado: {estado}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

# Conectar a MQTT
def conectar_mqtt():
    global client
    try:
        print("Conectando a MQTT...")
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.set_callback(callback)  # Asignar la función callback para los mensajes
        client.connect()  # Conectar al broker MQTT
        print(f"Conectado a {MQTT_BROKER}")
        client.subscribe(MQTT_TOPIC_SUB)  # Suscribirse al tema
        print(f"Suscrito a {MQTT_TOPIC_SUB}")
    except Exception as e:
        print(f"Error de conexión MQTT: {e}")
        print("Reintentando conexión MQTT...")
        time.sleep(5)
        conectar_mqtt()  # Reintentar conexión si falla

# Programa principal
conectar_wifi()

# Intentamos conectar a MQTT de manera inicial
conectar_mqtt()

# Bucle principal
while True:
    try:
        # Enciende y apaga el LED cada 0.5 segundos
        laser_pin.on()  # Enciende el LED
        print("Láser ENCENDIDO")
        publicar_estado("ON")  # Publica el estado "ON"
        time.sleep(10)

        laser_pin.off()  # Apaga el LED
        print("Láser APAGADO")
        publicar_estado("OFF")  # Publica el estado "OFF"
        time.sleep(10)

        # Verifica si hay mensajes MQTT entrantes
        client.check_msg()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Intentando reconectar...")
        time.sleep(5)
        conectar_wifi()
        conectar_mqtt()