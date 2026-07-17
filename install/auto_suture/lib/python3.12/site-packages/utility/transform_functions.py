
# Utility functions for transformations

# -----------------------------------------------------------------------

# Imports
from geometry_msgs.msg import PoseStamped
from PyKDL import Frame, Rotation, Vector


# Pose(Stamped) to PyKDL
# eg:   PyKDL_frame = pose_to_pykdl(pose_stamped.pose)
def pose_to_pykdl(pose):

    frame = Frame(
        Rotation.Quaternion(
            pose.orientation.x,
            pose.orientation.y,
            pose.orientation.z,
            pose.orientation.w
        ),
        Vector(
            pose.position.x,
            pose.position.y,
            pose.position.z
        )
    )

    return frame