#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import time


# Configuración del cliente MQTT
broker_address = "localhost"
client = mqtt.Client("cliente2")
client.connect(broker_address)

# Función que se ejecuta cuando llega un mensaje
def on_message(client, userdata, message):
    # Obtener el mensaje como cadena de texto
    mensaje_recibido = str(message.payload.decode("utf-8"))
    # Convertir el mensaje JSON en un diccionario
    sensores = json.loads(mensaje_recibido)
    # Imprimir el diccionario recibido
    print("Mensaje recibido:", sensores)
    if(message.topic == "datos_1"):
        print(sensores["sensores"]["Temperatura"])


# Configurar la función "on_message" como callback para el cliente MQTT
client.on_message = on_message
# Suscribirse al topic "datos"
client.subscribe("datos_1")

# Iniciar el bucle para manejar los eventos del cliente MQTT


# Bucle para enviar mensajes
while True:
    client.loop_start() # start the loop
    # Mensaje a enviar como diccionario
    mensaje = {"robot1": 0.256,
               "robot2": 0.35
               }
    # Convertir el diccionario en JSON
    mensaje_json = json.dumps(mensaje)
    # Publicar el mensaje en el topic "datos"
    client.publish("datos_2", mensaje_json)
    # Detener el bucle del cliente MQTT
    time.sleep(1)
    client.loop_stop()