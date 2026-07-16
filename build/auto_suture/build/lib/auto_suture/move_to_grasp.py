
# Node that moves arm to the grasp position
# Asks ToolGraspPose node for the correct pose for given arm
# Sends command to move there
# -----------------------------------------------------------------------

# Imports

import sys
import rclpy
from rclpy.node import Node
from auto_suture_interfaces.srv import FindGraspPose

# Define node
class MoveToGrasp(Node):

    def __init__(self):
        super().__init__('move_to_grasp')

        # Service client to calculate grasp pose
        self.cli = self.create_client(
            FindGraspPose,
            'find_grasp_pose',
        )
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = FindGraspPose.Request()

    def send_request(self, psm, grasp_type):
        self.req.psm = psm
        self.req.grasp_type = grasp_type
        return self.cli.call_async(self.req)

def main():
    rclpy.init()

    node = MoveToGrasp()
    future = node.send_request(str(sys.argv[1]), str(sys.argv[2]))
    rclpy.spin_until_future_complete(node, future)
    response = future.result()
    node.get_logger().info(
        f'Grasp position returned:\n{response}'
    )

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()