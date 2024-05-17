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
        client.subscribe(mqtt_topic)
    else:
        rospy.loginfo(f"Error al conectar al broker MQTT: {rc}")

def on_message(client, userdata, message):
    # Obtener el mensaje como cadena de texto
    mensaje_recibido = str(message.payload.decode("utf-8"))
    # Convertir el mensaje JSON en un diccionario
    mensaje_json = json.loads(mensaje_recibido)
    # Crear un mensaje LaserScan
    scan_msg = LaserScan()
    scan_msg.header.stamp = rospy.Time.now()
    scan_msg.header.frame_id = "map"  # Cambia "laser_frame" según el marco de referencia correcto
    scan_msg.angle_min = -3.14  # Ángulo mínimo del escaneo
    scan_msg.angle_max = 3.14   # Ángulo máximo del escaneo
    scan_msg.angle_increment = 0.0175  # Incremento angular
    scan_msg.time_increment = 0.0  # Incremento de tiempo entre escaneos
    scan_msg.scan_time = 0.1  # Duración del escaneo
    scan_msg.range_min = 0.0  # Rango mínimo del escaneo
    scan_msg.range_max = 10.0  # Rango máximo del escaneo
    scan_msg.ranges = mensaje_json["scan_data"]  # Datos del escaneo
    # Publicar el mensaje LaserScan en el tópico "/mapeo_nubes"
    lidar_pub.publish(scan_msg)

if __name__ == '__main__':
    rospy.init_node('lidar_publisher', anonymous=True)

    # Configurar el cliente MQTT
    client = mqtt.Client(client_id="Lidar_Subscriber", protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar al broker MQTT
    client.connect(mqtt_broker, mqtt_port, 60)

    # Crear el publicador para el mensaje LaserScan en el tópico "/mapeo_nubes"
    lidar_pub = rospy.Publisher('/mapeo_nubes', LaserScan, queue_size=10)

    # Iniciar el bucle para manejar los eventos del cliente MQTT
    client.loop_start()

    # Mantener el programa en ejecución
    rospy.spin()

    # Detener el bucle de eventos MQTT cuando se cierre el nodo ROS
    client.loop_stop()
