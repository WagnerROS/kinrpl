#!/usr/bin/env python3

import rospy
import paho.mqtt.client as mqtt
from std_msgs.msg import String

# Configuración del cliente MQTT
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "mqtt_topic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        rospy.loginfo("Conectado al broker MQTT")
        client.subscribe(mqtt_topic)
    else:
        rospy.loginfo(f"Error al conectar al broker MQTT: {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    rospy.loginfo(f"Mensaje recibido de MQTT: {message}")
    ros_msg = String()
    ros_msg.data = message
    pub.publish(ros_msg)

if __name__ == '__main__':
    rospy.init_node('mqtt_subscriber', anonymous=True)
    pub = rospy.Publisher("ros_topic", String, queue_size=10)
    
    client = mqtt.Client(client_id="Central_Nodo_Subscriber", protocol=mqtt.MQTTv311)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
    except Exception as e:
        rospy.logerr(f"No se pudo conectar al broker MQTT: {e}")
        exit(1)

    client.loop_start()

    rospy.spin()
