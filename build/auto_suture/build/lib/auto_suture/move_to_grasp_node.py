import sys
import rclpy
from rclpy.node import Node

from auto_suture_interfaces.srv import FindGraspPose
from geometry_msgs.msg import PoseStamped


class MoveToGrasp(Node):

    def __init__(self):
        super().__init__('move_to_grasp')

        self.cli = self.create_client(
            FindGraspPose,
            'find_grasp_pose'
        )

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'service not available, waiting again...'
            )

        self.req = FindGraspPose.Request()

        self.publisher_ = self.create_publisher(
            PoseStamped,
            '/CRTK/psm2/move_cp',
            10
        )


    def send_request(self, psm, grasp_type):
        self.req.psm = psm
        self.req.grasp_type = grasp_type
        return self.cli.call_async(self.req)


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

    response = future.result()

    if response.success:
        node.get_logger().info(
            f'Grasp position returned:\n{response.grasp_pose}'
        )

        node.publisher_.publish(response.grasp_pose)

    else:
        node.get_logger().error(
            f"Failed to find grasp pose: {response.message}"
        )

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()