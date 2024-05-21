# #!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class RobotMotionController(Node):
    def __init__(self):
        super().__init__('robot_motion_controller')
        self.joint_states_publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.rate = self.create_rate(10)
        self.joint_states = JointState()
        self.target_angles = [0, 0, 0, 0]
        self.current_angles = [0, 0, 0, 0]


    def move_angle(self, angles, speed):
        self.target_angles = angles

        self.joint_states.name = ['base_link1_joint', 'link1_link12_joint', 'link2_link23_joint', 'link3_link34_joint']
        current_index = 0

        while rclpy.ok():
            if current_index >= len(self.target_angles):
                print("Done")
                break

            target_angle = self.target_angles[current_index]

            current_angle = self.current_angles[current_index]
            if abs(current_angle - target_angle) >= 0.01:
                
                direction = math.copysign(1, target_angle - current_angle)
                new_angle = current_angle + direction * speed

                self.joint_states.position = [new_angle if j == current_index else float(self.current_angles[j]) for j in range(4)]
                self.current_angles = [new_angle if j == current_index else float(self.current_angles[j]) for j in range(4)]
                self.joint_states.header.stamp = self.get_clock().now().to_msg()

                print(self.current_angles, self.joint_states, end = "\n\n", sep="\n")
                self.joint_states_publisher.publish(self.joint_states)

            else:
                current_index += 1

def main():
    rclpy.init()
    controller = RobotMotionController()

    # Example: move to target angles [0, 1.57, 0, 0]
    target_angles = [int(input(f"Enter the angle (in radians - b/w -1 and 1) of link {i+1} : ")) for i in range(4)]
    speed = 0.0001  # Adjust the speed of motion
    controller.move_angle([0,0,0,0], speed)
    controller.move_angle(target_angles, speed)

    rclpy.spin(controller)

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
