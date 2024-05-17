#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import time

# Variables globales
global diccionario

# Configuración del cliente MQTT
broker_address = "localhost"
client = mqtt.Client("Central_Nodo")
client.connect(broker_address)

# Función que se ejecuta cuando llega un mensaje
def on_message(client, userdata, message):
    global diccionario
    # Obtener el mensaje como cadena de texto
    mensaje_recibido = str(message.payload.decode("utf-8"))
    # Convertir el mensaje JSON en un diccionario
    diccionario = json.loads(mensaje_recibido)
    # Imprimir el diccionario recibido
    print("Mensaje recibido:", diccionario)
    if(message.topic == "datos_2"):
        print(diccionario["robot1"])

# Configurar la función "on_message" como callback para el cliente MQTT
client.on_message = on_message
# Suscribirse al topic "datos_2"
client.subscribe("datos_2")

# Iniciar el bucle para manejar los eventos del cliente MQTT
# Bucle para enviar mensajes
while True:
    client.loop_start() # start the loop
    # Mensaje a enviar como diccionario
    mensaje = {"sensores": {
                            "Temperatura": "activado"

                            },
              "actuadores":"funcionando"       
               }
    # Convertir el diccionario en JSON
    mensaje_json = json.dumps(mensaje)
    # Publicar el mensaje en el topic "datos"
    client.publish("datos_1", mensaje_json)
    time.sleep(1)
    client.loop_stop()