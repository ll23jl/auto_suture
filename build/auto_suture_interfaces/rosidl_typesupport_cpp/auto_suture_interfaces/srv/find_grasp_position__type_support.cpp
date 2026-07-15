// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from auto_suture_interfaces:srv/FindGraspPosition.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"
#include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace auto_suture_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FindGraspPosition_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FindGraspPosition_Request_type_support_ids_t;

static const _FindGraspPosition_Request_type_support_ids_t _FindGraspPosition_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FindGraspPosition_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FindGraspPosition_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FindGraspPosition_Request_type_support_symbol_names_t _FindGraspPosition_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, auto_suture_interfaces, srv, FindGraspPosition_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, auto_suture_interfaces, srv, FindGraspPosition_Request)),
  }
};

typedef struct _FindGraspPosition_Request_type_support_data_t
{
  void * data[2];
} _FindGraspPosition_Request_type_support_data_t;

static _FindGraspPosition_Request_type_support_data_t _FindGraspPosition_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FindGraspPosition_Request_message_typesupport_map = {
  2,
  "auto_suture_interfaces",
  &_FindGraspPosition_Request_message_typesupport_ids.typesupport_identifier[0],
  &_FindGraspPosition_Request_message_typesupport_symbol_names.symbol_name[0],
  &_FindGraspPosition_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t FindGraspPosition_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FindGraspPosition_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Request>()
{
  return &::auto_suture_interfaces::srv::rosidl_typesupport_cpp::FindGraspPosition_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, auto_suture_interfaces, srv, FindGraspPosition_Request)() {
  return get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace auto_suture_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FindGraspPosition_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FindGraspPosition_Response_type_support_ids_t;

static const _FindGraspPosition_Response_type_support_ids_t _FindGraspPosition_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FindGraspPosition_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FindGraspPosition_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FindGraspPosition_Response_type_support_symbol_names_t _FindGraspPosition_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, auto_suture_interfaces, srv, FindGraspPosition_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, auto_suture_interfaces, srv, FindGraspPosition_Response)),
  }
};

typedef struct _FindGraspPosition_Response_type_support_data_t
{
  void * data[2];
} _FindGraspPosition_Response_type_support_data_t;

static _FindGraspPosition_Response_type_support_data_t _FindGraspPosition_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FindGraspPosition_Response_message_typesupport_map = {
  2,
  "auto_suture_interfaces",
  &_FindGraspPosition_Response_message_typesupport_ids.typesupport_identifier[0],
  &_FindGraspPosition_Response_message_typesupport_symbol_names.symbol_name[0],
  &_FindGraspPosition_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t FindGraspPosition_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FindGraspPosition_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Response>()
{
  return &::auto_suture_interfaces::srv::rosidl_typesupport_cpp::FindGraspPosition_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, auto_suture_interfaces, srv, FindGraspPosition_Response)() {
  return get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace auto_suture_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FindGraspPosition_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FindGraspPosition_Event_type_support_ids_t;

static const _FindGraspPosition_Event_type_support_ids_t _FindGraspPosition_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FindGraspPosition_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FindGraspPosition_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FindGraspPosition_Event_type_support_symbol_names_t _FindGraspPosition_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, auto_suture_interfaces, srv, FindGraspPosition_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, auto_suture_interfaces, srv, FindGraspPosition_Event)),
  }
};

typedef struct _FindGraspPosition_Event_type_support_data_t
{
  void * data[2];
} _FindGraspPosition_Event_type_support_data_t;

static _FindGraspPosition_Event_type_support_data_t _FindGraspPosition_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FindGraspPosition_Event_message_typesupport_map = {
  2,
  "auto_suture_interfaces",
  &_FindGraspPosition_Event_message_typesupport_ids.typesupport_identifier[0],
  &_FindGraspPosition_Event_message_typesupport_symbol_names.symbol_name[0],
  &_FindGraspPosition_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t FindGraspPosition_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FindGraspPosition_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Event>()
{
  return &::auto_suture_interfaces::srv::rosidl_typesupport_cpp::FindGraspPosition_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, auto_suture_interfaces, srv, FindGraspPosition_Event)() {
  return get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace auto_suture_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FindGraspPosition_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FindGraspPosition_type_support_ids_t;

static const _FindGraspPosition_type_support_ids_t _FindGraspPosition_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FindGraspPosition_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FindGraspPosition_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FindGraspPosition_type_support_symbol_names_t _FindGraspPosition_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, auto_suture_interfaces, srv, FindGraspPosition)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, auto_suture_interfaces, srv, FindGraspPosition)),
  }
};

typedef struct _FindGraspPosition_type_support_data_t
{
  void * data[2];
} _FindGraspPosition_type_support_data_t;

static _FindGraspPosition_type_support_data_t _FindGraspPosition_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FindGraspPosition_service_typesupport_map = {
  2,
  "auto_suture_interfaces",
  &_FindGraspPosition_service_typesupport_ids.typesupport_identifier[0],
  &_FindGraspPosition_service_typesupport_symbol_names.symbol_name[0],
  &_FindGraspPosition_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t FindGraspPosition_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FindGraspPosition_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<auto_suture_interfaces::srv::FindGraspPosition>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<auto_suture_interfaces::srv::FindGraspPosition>,
  &auto_suture_interfaces__srv__FindGraspPosition__get_type_hash,
  &auto_suture_interfaces__srv__FindGraspPosition__get_type_description,
  &auto_suture_interfaces__srv__FindGraspPosition__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition>()
{
  return &::auto_suture_interfaces::srv::rosidl_typesupport_cpp::FindGraspPosition_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, auto_suture_interfaces, srv, FindGraspPosition)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<auto_suture_interfaces::srv::FindGraspPosition>();
}

#ifdef __cplusplus
}
#endif
