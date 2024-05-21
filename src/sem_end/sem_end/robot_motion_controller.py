#!/usr/bin/env python

from turtle import distance
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
import math

class RobotMotionController(Node):
    def __init__(self):
        super().__init__('robot_motion_controller')
        self.joint_states_publisher = self.create_publisher(JointState, '/joint_states', 00)
        self.rate = self.create_rate(1000)
        self.joint_states = JointState()

    def move_point(self, target_x, target_y, angular_speed, linear_speed):
        self.joint_states.name = ['base_wheel1_joint', 'base_wheel2_joint']
        time = 0

        target_angle = math.atan2(target_y,target_x)
        rotation_time = target_angle/angular_speed

        distance = math.sqrt(target_x**2 + target_y**2)

        while rclpy.ok():

            time += 0.001

            left_wheel_speed = -angular_speed
            right_wheel_speed = +angular_speed

            self.joint_states.position = [time * - left_wheel_speed, time * - right_wheel_speed]
            self.joint_states.header.stamp = self.get_clock().now().to_msg()

            self.joint_states_publisher.publish(self.joint_states)
            # print(self.joint_states.header.stamp, "\t", self.joint_states.position)
            print(self.joint_states.position)

            if time > rotation_time:
                break
        
        while rclpy.ok():
            
            time += 0.001
            
            self.joint_states.position = [time * - linear_speed, time * - linear_speed]
            self.joint_states.header.stamp = self.get_clock().now().to_msg()

            self.joint_states_publisher.publish(self.joint_states)
            # print(self.joint_states.header.stamp, "\t", self.joint_states.position)
            print(self.joint_states.position)

            if time >= distance / linear_speed:
                print("Destination point (", target_x, target_y, ") reached")
                break



    def move_circle(self, radius, speed, body_width):
        self.joint_states.name = ['base_wheel1_joint', 'base_wheel2_joint']
        time = 0

        while rclpy.ok():

            time += 0.01

            if radius!=0:
                angular_speed = speed / radius
            else:
                angular_speed = speed
            left_wheel_speed = angular_speed * (radius - body_width)
            right_wheel_speed = angular_speed * (radius + body_width)

            self.joint_states.position = [time * - left_wheel_speed, time * - right_wheel_speed]
            self.joint_states.header.stamp = self.get_clock().now().to_msg()

            self.joint_states_publisher.publish(self.joint_states)
            # print(self.joint_states.header.stamp, "\t", self.joint_states.position)
            print(self.joint_states.position)

            # if time > (math.pi * radius**2)/angular_speed:
            #     break

    def move_straight(self, distance, speed):
        self.joint_states.name = ['base_wheel1_joint', 'base_wheel2_joint']
        time = 0

        while rclpy.ok():
            
            time += 0.001
            
            self.joint_states.position = [time * - speed, time * -speed]
            self.joint_states.header.stamp = self.get_clock().now().to_msg()

            self.joint_states_publisher.publish(self.joint_states)
            # print(self.joint_states.header.stamp, "\t", self.joint_states.position)
            print(self.joint_states.position)

            if time >= distance / speed:
                break

def main():
    rclpy.init()
    controller = RobotMotionController()

    controller.move_point(0, 10, 0.1, 0.3)

    # Move in a circle
    circle_radius = 1.0  # meters
    circle_speed = 0.1  # meters per second
    controller.move_circle(circle_radius, circle_speed, 0.2)

    # Move in a straight line
    straight_distance = 10.0  # meters
    straight_speed = 0.3  # meters per second
    controller.move_straight(straight_distance, straight_speed)

    rclpy.spin(controller)

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
