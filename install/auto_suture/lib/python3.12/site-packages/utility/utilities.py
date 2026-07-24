
from PyKDL import Vector, Rotation, Frame, dot
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, posestamped_to_pykdl, pykdl_to_posestamped


# ---------- Interpolation Function (by me) ----------
def cartesian_interpolate_step(T_curr, T_goal,
                               max_translation=0.005,
                               max_rotation=0.1,
                               deadband=0.001):

    
    # Adjust deadband for rotation
    rot_deadband = deadband * 20

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

    return T_step, done, trans_error_mag, rot_error_mag, deadband, rot_deadband, max_translation, max_rotation


# ----------------------------------------------------------------------------------------

# # ---------- Interpolation Function (from Surgical Robotics Challenge) NO CHANGES ----------

# def cartesian_interpolate_step(T_curr, T_goal, max_delta=0.01, deadband=0.01):
#     error = np.zeros(6)
#     pe = T_goal.p - T_curr.p
#     re = (T_curr.M.Inverse() * T_goal.M).GetRPY()
#     for i in range(6):
#         if i < 3:
#             error[i] = pe[i]
#         else:
#             error[i] = re[i-3]

#     done = False
#     error_max = max(np.abs(error))
#     if error_max <= deadband:
#         error_scaled = error * 0.
#         done = True
#     else:
#         error_scaled = error / error_max

#     error_scaled = error_scaled * max_delta

#     T_step = Frame(Rotation.RPY(error_scaled[3], error_scaled[4], error_scaled[5]),
#                                 Vector(error_scaled[0], error_scaled[1], error_scaled[2]))
#     return T_step, done

# # ----------------------------------------------------------------------------------------

# # ---------- Interpolation Function (from Surgical Robotics Challenge) with error logging ----------

# def cartesian_interpolate_step(T_curr, T_goal, max_delta=0.005, deadband=0.005):
#     error = np.zeros(6)

#     # Position error
#     pe = T_goal.p - T_curr.p

#     # Rotation error (RPY)
#     re = (T_curr.M.Inverse() * T_goal.M).GetRPY()

#     # Assemble 6D error vector
#     for i in range(6):
#         if i < 3:
#             error[i] = pe[i]
#         else:
#             error[i] = re[i - 3]

#     # Individual error magnitudes (for logging)
#     trans_error_mag = np.linalg.norm(error[:3])
#     rot_error_mag = np.linalg.norm(error[3:])

#     # Original SRC interpolation logic
#     done = False
#     error_max = np.max(np.abs(error))

#     if error_max <= deadband:
#         error_scaled = np.zeros(6)
#         done = True
#     else:
#         error_scaled = error / error_max

#     error_scaled *= max_delta

#     T_step = Frame(
#         Rotation.RPY(
#             error_scaled[3],
#             error_scaled[4],
#             error_scaled[5]
#         ),
#         Vector(
#             error_scaled[0],
#             error_scaled[1],
#             error_scaled[2]
#         )
#     )

#     return T_step, done, trans_error_mag, rot_error_mag, deadband, deadband, max_delta, max_delta

# # ----------------------------------------------------------------------------------------



# ---------- Function that tracks errors and plots against time ----------
def save_error_plot(
    step_name,
    times,
    trans_errors,
    rot_errors,
    deadband,
    rot_deadband,
    max_translation,
    max_rotation,
    success,
    save_dir="/home/jazmin/auto_suture/src/auto_suture/data",
):
    """
    Save a translation/rotation error plot for one controller run.

    Parameters
    ----------
    step_name : str
        e.g. "Pick Up Needle"
    success : bool
        True if the target was reached, False if aborted.
    """

    # Create a folder for this step
    step_dir = os.path.join(
        save_dir,
        step_name.lower().replace(" ", "_")
    )
    os.makedirs(step_dir, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax2 = ax1.twinx()

    line1 = ax1.plot(
        times,
        trans_errors,
        linewidth=1,
        label="Translation Error",
        color="b"
    )

    line2 = ax2.plot(
        times,
        rot_errors,
        linewidth=1,
        label="Rotation Error",
        color="r"
    )

    ax1.axhline(
        deadband,
        linestyle="--",
        linewidth=1,
        label="Translation deadband",
        color="b"
    )

    ax2.axhline(
        rot_deadband,
        linestyle="--",
        linewidth=1,
        label="Rotation deadband",
        color="r"
    )

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Translation Error (m)")
    ax2.set_ylabel("Rotation Error (rad)")
    ax1.grid(True)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels)

    plt.title(step_name)

    parameters = (
        f"Translation deadband : {deadband:.4f} m\n"
        f"Rotation deadband    : {rot_deadband:.4f} rad\n"
        f"Max translation step : {max_translation:.4f} m\n"
        f"Max rotation step    : {max_rotation:.4f} rad\n"
        f"Runtime              : {times[-1]:.2f} s\n"
        f"Iterations           : {len(times)}\n"
        f"Final trans. error   : {trans_errors[-1]:.4f} m\n"
        f"Final rot. error     : {rot_errors[-1]:.4f} rad\n"
        f"Status               : {'Success' if success else 'Aborted'}"
    )

    fig.text(
        0.0,
        0.0,
        parameters,
        fontsize=9,
        family="monospace",
        va="bottom",
        bbox=dict(facecolor="whitesmoke", edgecolor="gray")
    )

    fig.tight_layout(rect=[0, 0.2, 1, 1])

    filename = (
        datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".png"
    )

    filepath = os.path.join(step_dir, filename)

    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return filepath