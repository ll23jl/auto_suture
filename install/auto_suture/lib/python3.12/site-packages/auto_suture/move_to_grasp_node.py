import sys
import rclpy
from rclpy.node import Node
import time

from auto_suture_interfaces.srv import FindGraspPose
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState


class MoveToGrasp(Node):

    def __init__(self):
        super().__init__('move_to_grasp')

        # Service Client to find grasp pose
        self.cli = self.create_client(
            FindGraspPose,
            'find_grasp_pose'
        )

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'service not available, waiting again...'
            )

        self.req = FindGraspPose.Request()

        # publisher to move the arm
        self.arm_pub = self.create_publisher(
            PoseStamped,
            '/CRTK/psm2/move_cp',
            10
        )

        # publisher to move jaw
        self.jaw_pub = self.create_publisher(
            JointState,
            '/CRTK/psm2/jaw/servo_jp',
            10
        )

    # function that sends request for grasp position with given parameters (psm and grasp type)
    def send_request(self, psm, grasp_type):

        req = FindGraspPose.Request()
        req.psm = psm
        req.grasp_type = grasp_type

        return self.cli.call_async(req)


def main():

    rclpy.init()

    node = MoveToGrasp()

    if len(sys.argv) < 3:
        node.get_logger().error(
            "Usage: ros2 run auto_suture move_to_grasp <psm> <grasp_type>"
        )
        return

    future = node.send_request(
        sys.argv[1],
        sys.argv[2]
    )

    rclpy.spin_until_future_complete(node, future)

    # store response
    response = future.result()

    if response.success:
        node.get_logger().info(
            f'Approach position returned:\n{response.approach_pose}'
        )

        # send approach pose to robot
        node.arm_pub.publish(response.approach_pose)

        # wait
        for _ in range(10):
            rclpy.spin_once(node, timeout_sec=0.1) 

        node.get_logger().info(
            f'Grasp position returned:\n{response.grasp_pose}'
        )

        # send grasp pose to robot
        node.arm_pub.publish(response.grasp_pose)

        # wait
        for _ in range(10):
            rclpy.spin_once(node, timeout_sec=0.1) 

        # close jaws
        jaw_pos = JointState()
        jaw_pos.header.stamp = node.get_clock().now().to_msg()
        jaw_pos.name = ["jaw"]
        jaw_pos.position = [0.0]

        node.jaw_pub.publish(jaw_pos)
        
        node.get_logger().info("Closing jaws")

    else:
        node.get_logger().error(
            f"Failed to find grasp pose: {response.message}"
        )

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()