// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from auto_suture_interfaces:srv/FindGraspPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "auto_suture_interfaces/srv/find_grasp_pose.h"


#ifndef AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSE__STRUCT_H_
#define AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'psm'
// Member 'grasp_type'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/FindGraspPose in the package auto_suture_interfaces.
typedef struct auto_suture_interfaces__srv__FindGraspPose_Request
{
  rosidl_runtime_c__String psm;
  rosidl_runtime_c__String grasp_type;
} auto_suture_interfaces__srv__FindGraspPose_Request;

// Struct for a sequence of auto_suture_interfaces__srv__FindGraspPose_Request.
typedef struct auto_suture_interfaces__srv__FindGraspPose_Request__Sequence
{
  auto_suture_interfaces__srv__FindGraspPose_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} auto_suture_interfaces__srv__FindGraspPose_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'grasp_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/FindGraspPose in the package auto_suture_interfaces.
typedef struct auto_suture_interfaces__srv__FindGraspPose_Response
{
  geometry_msgs__msg__PoseStamped grasp_pose;
  bool success;
  rosidl_runtime_c__String message;
} auto_suture_interfaces__srv__FindGraspPose_Response;

// Struct for a sequence of auto_suture_interfaces__srv__FindGraspPose_Response.
typedef struct auto_suture_interfaces__srv__FindGraspPose_Response__Sequence
{
  auto_suture_interfaces__srv__FindGraspPose_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} auto_suture_interfaces__srv__FindGraspPose_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  auto_suture_interfaces__srv__FindGraspPose_Event__request__MAX_SIZE = 1
};
// response
enum
{
  auto_suture_interfaces__srv__FindGraspPose_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/FindGraspPose in the package auto_suture_interfaces.
typedef struct auto_suture_interfaces__srv__FindGraspPose_Event
{
  service_msgs__msg__ServiceEventInfo info;
  auto_suture_interfaces__srv__FindGraspPose_Request__Sequence request;
  auto_suture_interfaces__srv__FindGraspPose_Response__Sequence response;
} auto_suture_interfaces__srv__FindGraspPose_Event;

// Struct for a sequence of auto_suture_interfaces__srv__FindGraspPose_Event.
typedef struct auto_suture_interfaces__srv__FindGraspPose_Event__Sequence
{
  auto_suture_interfaces__srv__FindGraspPose_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} auto_suture_interfaces__srv__FindGraspPose_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSE__STRUCT_H_
