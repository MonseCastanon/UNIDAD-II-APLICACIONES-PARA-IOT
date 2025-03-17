import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración del receptor IR
IR_PIN = 15  
ir_receiver = machine.Pin(IR_PIN, machine.Pin.IN)

# Configuración WiFi
WIFI_SSID = 'RaspBerry 7'
WIFI_PASSWORD = 'linux4321'

# Configuración MQTT
MQTT_BROKER = '192.168.137.164'
MQTT_PORT = 1883
MQTT_TOPIC = 'receptor_infrarojo'

# Conectar a WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print('Conectado a WiFi:', wlan.ifconfig())
    else:
        print('Error: No se pudo conectar a WiFi')
        machine.reset()

# Conectar WiFi
connect_wifi()

# Cliente MQTT
client = MQTTClient('ESP32_client', MQTT_BROKER, port=MQTT_PORT, keepalive=60)
client.connect()

# Captura de señal IR optimizada
def recibir_senal():
    tiempo_inicial = time.ticks_us()

    while ir_receiver.value() == 0:  # Esperar inicio
        pass
    
    while ir_receiver.value() == 1:  # Medir duración
        pass

    duracion = time.ticks_diff(time.ticks_us(), tiempo_inicial)
    return duracion

# Bucle principal
try:
    while True:
        if ir_receiver.value() == 0:  
            duracion = recibir_senal()
            mensaje = f"Señal IR: {duracion} us"
            print(mensaje)
            client.publish(MQTT_TOPIC, mensaje.encode())  
            time.sleep(0.2)

except KeyboardInterrupt:
    print("Programa detenido por el usuario")
    client.disconnect()