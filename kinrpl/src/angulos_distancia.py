#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

class SpecificPublisher:
    def __init__(self):
        rospy.init_node('specific_publisher')

        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.specific_pub = rospy.Publisher('/specific', Float32, queue_size=10)

    def scan_callback(self, data):
        angles = [0, 30, 60, 90, 120, 150, 180]
        specific_distances = [data.ranges[int(angle * len(data.ranges) / 360)] for angle in angles]

        for i, angle in enumerate(angles):
            rospy.loginfo("Angle {}: {} meters".format(angle, specific_distances[i]))
            specific_distance_msg = Float32()
            specific_distance_msg.data = specific_distances[i]
            self.specific_pub.publish(specific_distance_msg)

if __name__ == '__main__':
    try:
        SpecificPublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
