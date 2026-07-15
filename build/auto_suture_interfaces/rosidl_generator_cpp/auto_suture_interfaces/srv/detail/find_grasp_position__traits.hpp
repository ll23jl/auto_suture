// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from auto_suture_interfaces:srv/FindGraspPosition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "auto_suture_interfaces/srv/find_grasp_position.hpp"


#ifndef AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSITION__TRAITS_HPP_
#define AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSITION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace auto_suture_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const FindGraspPosition_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: psm
  {
    out << "psm: ";
    rosidl_generator_traits::value_to_yaml(msg.psm, out);
    out << ", ";
  }

  // member: grasp_type
  {
    out << "grasp_type: ";
    rosidl_generator_traits::value_to_yaml(msg.grasp_type, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FindGraspPosition_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: psm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "psm: ";
    rosidl_generator_traits::value_to_yaml(msg.psm, out);
    out << "\n";
  }

  // member: grasp_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "grasp_type: ";
    rosidl_generator_traits::value_to_yaml(msg.grasp_type, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FindGraspPosition_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use auto_suture_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const auto_suture_interfaces::srv::FindGraspPosition_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  auto_suture_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use auto_suture_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const auto_suture_interfaces::srv::FindGraspPosition_Request & msg)
{
  return auto_suture_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<auto_suture_interfaces::srv::FindGraspPosition_Request>()
{
  return "auto_suture_interfaces::srv::FindGraspPosition_Request";
}

template<>
inline const char * name<auto_suture_interfaces::srv::FindGraspPosition_Request>()
{
  return "auto_suture_interfaces/srv/FindGraspPosition_Request";
}

template<>
struct has_fixed_size<auto_suture_interfaces::srv::FindGraspPosition_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<auto_suture_interfaces::srv::FindGraspPosition_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'grasp_pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace auto_suture_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const FindGraspPosition_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: grasp_pose
  {
    out << "grasp_pose: ";
    to_flow_style_yaml(msg.grasp_pose, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FindGraspPosition_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: grasp_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "grasp_pose:\n";
    to_block_style_yaml(msg.grasp_pose, out, indentation + 2);
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FindGraspPosition_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use auto_suture_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const auto_suture_interfaces::srv::FindGraspPosition_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  auto_suture_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use auto_suture_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const auto_suture_interfaces::srv::FindGraspPosition_Response & msg)
{
  return auto_suture_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<auto_suture_interfaces::srv::FindGraspPosition_Response>()
{
  return "auto_suture_interfaces::srv::FindGraspPosition_Response";
}

template<>
inline const char * name<auto_suture_interfaces::srv::FindGraspPosition_Response>()
{
  return "auto_suture_interfaces/srv/FindGraspPosition_Response";
}

template<>
struct has_fixed_size<auto_suture_interfaces::srv::FindGraspPosition_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<auto_suture_interfaces::srv::FindGraspPosition_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace auto_suture_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const FindGraspPosition_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FindGraspPosition_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FindGraspPosition_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace auto_suture_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use auto_suture_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const auto_suture_interfaces::srv::FindGraspPosition_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  auto_suture_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use auto_suture_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const auto_suture_interfaces::srv::FindGraspPosition_Event & msg)
{
  return auto_suture_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<auto_suture_interfaces::srv::FindGraspPosition_Event>()
{
  return "auto_suture_interfaces::srv::FindGraspPosition_Event";
}

template<>
inline const char * name<auto_suture_interfaces::srv::FindGraspPosition_Event>()
{
  return "auto_suture_interfaces/srv/FindGraspPosition_Event";
}

template<>
struct has_fixed_size<auto_suture_interfaces::srv::FindGraspPosition_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Event>
  : std::integral_constant<bool, has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Request>::value && has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<auto_suture_interfaces::srv::FindGraspPosition_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<auto_suture_interfaces::srv::FindGraspPosition>()
{
  return "auto_suture_interfaces::srv::FindGraspPosition";
}

template<>
inline const char * name<auto_suture_interfaces::srv::FindGraspPosition>()
{
  return "auto_suture_interfaces/srv/FindGraspPosition";
}

template<>
struct has_fixed_size<auto_suture_interfaces::srv::FindGraspPosition>
  : std::integral_constant<
    bool,
    has_fixed_size<auto_suture_interfaces::srv::FindGraspPosition_Request>::value &&
    has_fixed_size<auto_suture_interfaces::srv::FindGraspPosition_Response>::value
  >
{
};

template<>
struct has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition>
  : std::integral_constant<
    bool,
    has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Request>::value &&
    has_bounded_size<auto_suture_interfaces::srv::FindGraspPosition_Response>::value
  >
{
};

template<>
struct is_service<auto_suture_interfaces::srv::FindGraspPosition>
  : std::true_type
{
};

template<>
struct is_service_request<auto_suture_interfaces::srv::FindGraspPosition_Request>
  : std::true_type
{
};

template<>
struct is_service_response<auto_suture_interfaces::srv::FindGraspPosition_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSITION__TRAITS_HPP_
