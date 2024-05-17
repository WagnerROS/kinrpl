#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import paho.mqtt.client as mqtt
import json

# Configuración del cliente MQTT
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "LidarA1"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        rospy.loginfo("Conectado al broker MQTT")
    else:
        rospy.loginfo(f"Error al conectar al broker MQTT: {rc}")

def on_publish(client, userdata, mid):
    rospy.loginfo(f"Mensaje publicado con ID {mid}")

def lidar_callback(data):
    # Convertir los datos del escaneo a una lista
    scan_data = list(data.ranges)
    # Crear un diccionario para el mensaje
    mensaje = {"scan_data": scan_data}
    # Convertir el diccionario a JSON
    mensaje_json = json.dumps(mensaje)
    # Publicar el mensaje en el tópico MQTT
    client.publish(mqtt_topic, mensaje_json)

if __name__ == '__main__':
    rospy.init_node('lidar_publisher', anonymous=True)

    # Configurar el cliente MQTT
    client = mqtt.Client(client_id="Lidar_Publisher", protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Conectar al broker MQTT
    client.connect(mqtt_broker, mqtt_port, 60)

    # Suscribirse al tópico del escaneo del LiDAR
    rospy.Subscriber("/scan", LaserScan, lidar_callback)

    # Iniciar el bucle para manejar los eventos del cliente MQTT
    client.loop_start()

    # Mantener el programa en ejecución
    rospy.spin()

    # Detener el bucle de eventos MQTT cuando se cierre el nodo ROS
    client.loop_stop()
