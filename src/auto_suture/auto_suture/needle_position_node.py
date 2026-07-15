import rclpy
from rclpy.node import Node

from ambf_msgs.msg import RigidBodyState
from geometry_msgs.msg import PoseStamped


# Needle position node definition
class NeedlePosition(Node):

    def __init__(self):
        super().__init__('needle_position')

        # Subscriber
        self.subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Needle/State',
            self.state_callback,
            10
        )

        # Publisher
        self.publisher_ = self.create_publisher(
            PoseStamped,
            '/needle_position',
            10
        )
    def state_callback(self, msg):

        # Create a new outgoing message
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose.position = msg.pose.position
        pose.pose.orientation = msg.pose.orientation

        # Publish
        self.publisher_.publish(pose)

        self.get_logger().debug(
            f"Needle position: "
            f"({pose.pose.position.x:.3f}, "
            f"{pose.pose.position.y:.3f}, "
            f"{pose.pose.position.z:.3f})"
        )
    

def main(args=None):
    rclpy.init(args=args)

    needle_position = NeedlePosition()

    rclpy.spin(needle_position)

    # Destroy the node explicitly
    needle_position.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()