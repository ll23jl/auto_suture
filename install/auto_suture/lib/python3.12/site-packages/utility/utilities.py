
from PyKDL import Vector, Rotation, Frame, dot
import numpy as np
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, posestamped_to_pykdl, pykdl_to_posestamped

def cartesian_interpolate_step(T_curr, T_goal,
                               max_translation=0.005,
                               max_rotation=0.05,
                               deadband=0.001):

    
    # Adjust deadband for rotation
    rot_deadband = deadband * 10

    # Position error
    pe = T_goal.p - T_curr.p

    # Rotation error
    re = (T_curr.M.Inverse() * T_goal.M).GetRPY()

    # Translation step
    trans_error = np.array([pe[0], pe[1], pe[2]])
    trans_mag = np.linalg.norm(trans_error)

    if trans_mag < deadband:
        trans_step = np.zeros(3)
    else:
        trans_step = trans_error / trans_mag * min(trans_mag, max_translation)


    # Rotation step
    rot_error = np.array(re)
    rot_mag = np.linalg.norm(rot_error)

    if rot_mag < rot_deadband:
        rot_step = np.zeros(3)
    else:
        rot_step = rot_error / rot_mag * min(rot_mag, max_rotation)


    T_step = Frame(
        Rotation.RPY(
            rot_step[0],
            rot_step[1],
            rot_step[2]
        ),
        Vector(
            trans_step[0],
            trans_step[1],
            trans_step[2]
        )
    )

    done = (
        trans_mag < deadband and
        rot_mag < rot_deadband
    )

    trans_error_mag = np.linalg.norm(trans_error)
    rot_error_mag = np.linalg.norm(rot_error)

    return T_step, done, trans_error_mag, rot_error_mag