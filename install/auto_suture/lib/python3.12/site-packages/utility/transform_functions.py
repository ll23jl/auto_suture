
# Utility functions for transformations

# -----------------------------------------------------------------------

# Imports
from geometry_msgs.msg import PoseStamped, Pose
from PyKDL import Frame, Rotation, Vector

# -----------------------------------------------------------------------

# Pose to PyKDL
# eg:   PyKDL_frame = pose_to_pykdl(pose)
# or:   PyKDL_frame = pose_to_pykdl(posestamped.pose)
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

# -----------------------------------------------------------------------

# PoseStamped to PyKDL
def posestamped_to_pykdl(posestamped):
    return pose_to_pykdl(posestamped.pose)

# -----------------------------------------------------------------------

# PyKDL to Pose
def pykdl_to_pose(frame):
    
    pose = Pose()

    pose.position.x = frame.p.x()
    pose.position.y = frame.p.y()
    pose.position.z = frame.p.z()

    qx, qy, qz, qw = frame.M.GetQuaternion()

    pose.orientation.x = qx
    pose.orientation.y = qy
    pose.orientation.z = qz
    pose.orientation.w = qw

    return pose

# -----------------------------------------------------------------------

# PyKDL to PoseStamped
def pykdl_to_posestamped(frame, frame_id):

    posestamped = PoseStamped()

    posestamped.pose = pykdl_to_pose(frame)

    posestamped.header.frame_id = frame_id

    return posestamped

# -----------------------------------------------------------------------
