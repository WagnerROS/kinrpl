#!/usr/bin/env python3

import rospy
import paho.mqtt.client as mqtt
from std_msgs.msg import String

# Configuración del cliente MQTT
mqtt_broker = "localhost"  # Usar localhost para el broker en la misma máquina
mqtt_port = 1883
mqtt_topic = "mqtt_topic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        rospy.loginfo("Conectado al broker MQTT")
    else:
        rospy.loginfo(f"Error al conectar al broker MQTT: {rc}")

def on_publish(client, userdata, mid):
    rospy.loginfo(f"Mensaje publicado con ID {mid}")

def callback(data):
    msg = data.data
    client.publish(mqtt_topic, msg)
    rospy.loginfo(f"Publicado en MQTT: {msg}")

if __name__ == '__main__':
    rospy.init_node('mqtt_publisher', anonymous=True)
    client = mqtt.Client(client_id="Central_Nodo", protocol=mqtt.MQTTv311)

    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
    except Exception as e:
        rospy.logerr(f"No se pudo conectar al broker MQTT: {e}")
        exit(1)

    client.loop_start()

    rospy.Subscriber("ros_topic", String, callback)
    rospy.spin()
