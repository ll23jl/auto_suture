// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from auto_suture_interfaces:srv/FindGraspPosition.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "auto_suture_interfaces/srv/detail/find_grasp_position__rosidl_typesupport_introspection_c.h"
#include "auto_suture_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"
#include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  auto_suture_interfaces__srv__FindGraspPosition_Request__init(message_memory);
}

void auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_fini_function(void * message_memory)
{
  auto_suture_interfaces__srv__FindGraspPosition_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(auto_suture_interfaces__srv__FindGraspPosition_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_members = {
  "auto_suture_interfaces__srv",  // message namespace
  "FindGraspPosition_Request",  // message name
  1,  // number of fields
  sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request),
  false,  // has_any_key_member_
  auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_member_array,  // message members
  auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_type_support_handle = {
  0,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_members,
  get_message_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_auto_suture_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Request)() {
  if (!auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_type_support_handle.typesupport_identifier) {
    auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__rosidl_typesupport_introspection_c.h"
// already included above
// #include "auto_suture_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.h"


// Include directives for member types
// Member `grasp_pose`
#include "geometry_msgs/msg/pose_stamped.h"
// Member `grasp_pose`
#include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  auto_suture_interfaces__srv__FindGraspPosition_Response__init(message_memory);
}

void auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_fini_function(void * message_memory)
{
  auto_suture_interfaces__srv__FindGraspPosition_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_member_array[1] = {
  {
    "grasp_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(auto_suture_interfaces__srv__FindGraspPosition_Response, grasp_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_members = {
  "auto_suture_interfaces__srv",  // message namespace
  "FindGraspPosition_Response",  // message name
  1,  // number of fields
  sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response),
  false,  // has_any_key_member_
  auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_member_array,  // message members
  auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle = {
  0,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_members,
  get_message_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_auto_suture_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Response)() {
  auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  if (!auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle.typesupport_identifier) {
    auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__rosidl_typesupport_introspection_c.h"
// already included above
// #include "auto_suture_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "auto_suture_interfaces/srv/find_grasp_position.h"
// Member `request`
// Member `response`
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  auto_suture_interfaces__srv__FindGraspPosition_Event__init(message_memory);
}

void auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_fini_function(void * message_memory)
{
  auto_suture_interfaces__srv__FindGraspPosition_Event__fini(message_memory);
}

size_t auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__size_function__FindGraspPosition_Event__request(
  const void * untyped_member)
{
  const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * member =
    (const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_const_function__FindGraspPosition_Event__request(
  const void * untyped_member, size_t index)
{
  const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * member =
    (const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_function__FindGraspPosition_Event__request(
  void * untyped_member, size_t index)
{
  auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * member =
    (auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__fetch_function__FindGraspPosition_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto_suture_interfaces__srv__FindGraspPosition_Request * item =
    ((const auto_suture_interfaces__srv__FindGraspPosition_Request *)
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_const_function__FindGraspPosition_Event__request(untyped_member, index));
  auto_suture_interfaces__srv__FindGraspPosition_Request * value =
    (auto_suture_interfaces__srv__FindGraspPosition_Request *)(untyped_value);
  *value = *item;
}

void auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__assign_function__FindGraspPosition_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto_suture_interfaces__srv__FindGraspPosition_Request * item =
    ((auto_suture_interfaces__srv__FindGraspPosition_Request *)
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_function__FindGraspPosition_Event__request(untyped_member, index));
  const auto_suture_interfaces__srv__FindGraspPosition_Request * value =
    (const auto_suture_interfaces__srv__FindGraspPosition_Request *)(untyped_value);
  *item = *value;
}

bool auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__resize_function__FindGraspPosition_Event__request(
  void * untyped_member, size_t size)
{
  auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * member =
    (auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence *)(untyped_member);
  auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__fini(member);
  return auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__init(member, size);
}

size_t auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__size_function__FindGraspPosition_Event__response(
  const void * untyped_member)
{
  const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * member =
    (const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_const_function__FindGraspPosition_Event__response(
  const void * untyped_member, size_t index)
{
  const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * member =
    (const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_function__FindGraspPosition_Event__response(
  void * untyped_member, size_t index)
{
  auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * member =
    (auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__fetch_function__FindGraspPosition_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto_suture_interfaces__srv__FindGraspPosition_Response * item =
    ((const auto_suture_interfaces__srv__FindGraspPosition_Response *)
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_const_function__FindGraspPosition_Event__response(untyped_member, index));
  auto_suture_interfaces__srv__FindGraspPosition_Response * value =
    (auto_suture_interfaces__srv__FindGraspPosition_Response *)(untyped_value);
  *value = *item;
}

void auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__assign_function__FindGraspPosition_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto_suture_interfaces__srv__FindGraspPosition_Response * item =
    ((auto_suture_interfaces__srv__FindGraspPosition_Response *)
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_function__FindGraspPosition_Event__response(untyped_member, index));
  const auto_suture_interfaces__srv__FindGraspPosition_Response * value =
    (const auto_suture_interfaces__srv__FindGraspPosition_Response *)(untyped_value);
  *item = *value;
}

bool auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__resize_function__FindGraspPosition_Event__response(
  void * untyped_member, size_t size)
{
  auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * member =
    (auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence *)(untyped_member);
  auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__fini(member);
  return auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(auto_suture_interfaces__srv__FindGraspPosition_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(auto_suture_interfaces__srv__FindGraspPosition_Event, request),  // bytes offset in struct
    NULL,  // default value
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__size_function__FindGraspPosition_Event__request,  // size() function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_const_function__FindGraspPosition_Event__request,  // get_const(index) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_function__FindGraspPosition_Event__request,  // get(index) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__fetch_function__FindGraspPosition_Event__request,  // fetch(index, &value) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__assign_function__FindGraspPosition_Event__request,  // assign(index, value) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__resize_function__FindGraspPosition_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(auto_suture_interfaces__srv__FindGraspPosition_Event, response),  // bytes offset in struct
    NULL,  // default value
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__size_function__FindGraspPosition_Event__response,  // size() function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_const_function__FindGraspPosition_Event__response,  // get_const(index) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__get_function__FindGraspPosition_Event__response,  // get(index) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__fetch_function__FindGraspPosition_Event__response,  // fetch(index, &value) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__assign_function__FindGraspPosition_Event__response,  // assign(index, value) function pointer
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__resize_function__FindGraspPosition_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_members = {
  "auto_suture_interfaces__srv",  // message namespace
  "FindGraspPosition_Event",  // message name
  3,  // number of fields
  sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event),
  false,  // has_any_key_member_
  auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_member_array,  // message members
  auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_type_support_handle = {
  0,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_members,
  get_message_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_auto_suture_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Event)() {
  auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Request)();
  auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Response)();
  if (!auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_type_support_handle.typesupport_identifier) {
    auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "auto_suture_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_members = {
  "auto_suture_interfaces__srv",  // service namespace
  "FindGraspPosition",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_type_support_handle,
  NULL,  // response message
  // auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle
  NULL  // event_message
  // auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle
};


static rosidl_service_type_support_t auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_type_support_handle = {
  0,
  &auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_members,
  get_service_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__rosidl_typesupport_introspection_c__FindGraspPosition_Request_message_type_support_handle,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__rosidl_typesupport_introspection_c__FindGraspPosition_Response_message_type_support_handle,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__rosidl_typesupport_introspection_c__FindGraspPosition_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    auto_suture_interfaces,
    srv,
    FindGraspPosition
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    auto_suture_interfaces,
    srv,
    FindGraspPosition
  ),
  &auto_suture_interfaces__srv__FindGraspPosition__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_auto_suture_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition)(void) {
  if (!auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_type_support_handle.typesupport_identifier) {
    auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, auto_suture_interfaces, srv, FindGraspPosition_Event)()->data;
  }

  return &auto_suture_interfaces__srv__detail__find_grasp_position__rosidl_typesupport_introspection_c__FindGraspPosition_service_type_support_handle;
}
