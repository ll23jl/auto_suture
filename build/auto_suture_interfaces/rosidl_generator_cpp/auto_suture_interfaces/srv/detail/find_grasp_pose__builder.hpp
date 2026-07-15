// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from auto_suture_interfaces:srv/FindGraspPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "auto_suture_interfaces/srv/find_grasp_pose.hpp"


#ifndef AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSE__BUILDER_HPP_
#define AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "auto_suture_interfaces/srv/detail/find_grasp_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace auto_suture_interfaces
{

namespace srv
{

namespace builder
{

class Init_FindGraspPose_Request_grasp_type
{
public:
  explicit Init_FindGraspPose_Request_grasp_type(::auto_suture_interfaces::srv::FindGraspPose_Request & msg)
  : msg_(msg)
  {}
  ::auto_suture_interfaces::srv::FindGraspPose_Request grasp_type(::auto_suture_interfaces::srv::FindGraspPose_Request::_grasp_type_type arg)
  {
    msg_.grasp_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Request msg_;
};

class Init_FindGraspPose_Request_psm
{
public:
  Init_FindGraspPose_Request_psm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FindGraspPose_Request_grasp_type psm(::auto_suture_interfaces::srv::FindGraspPose_Request::_psm_type arg)
  {
    msg_.psm = std::move(arg);
    return Init_FindGraspPose_Request_grasp_type(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::auto_suture_interfaces::srv::FindGraspPose_Request>()
{
  return auto_suture_interfaces::srv::builder::Init_FindGraspPose_Request_psm();
}

}  // namespace auto_suture_interfaces


namespace auto_suture_interfaces
{

namespace srv
{

namespace builder
{

class Init_FindGraspPose_Response_message
{
public:
  explicit Init_FindGraspPose_Response_message(::auto_suture_interfaces::srv::FindGraspPose_Response & msg)
  : msg_(msg)
  {}
  ::auto_suture_interfaces::srv::FindGraspPose_Response message(::auto_suture_interfaces::srv::FindGraspPose_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Response msg_;
};

class Init_FindGraspPose_Response_success
{
public:
  explicit Init_FindGraspPose_Response_success(::auto_suture_interfaces::srv::FindGraspPose_Response & msg)
  : msg_(msg)
  {}
  Init_FindGraspPose_Response_message success(::auto_suture_interfaces::srv::FindGraspPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_FindGraspPose_Response_message(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Response msg_;
};

class Init_FindGraspPose_Response_grasp_pose
{
public:
  Init_FindGraspPose_Response_grasp_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FindGraspPose_Response_success grasp_pose(::auto_suture_interfaces::srv::FindGraspPose_Response::_grasp_pose_type arg)
  {
    msg_.grasp_pose = std::move(arg);
    return Init_FindGraspPose_Response_success(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::auto_suture_interfaces::srv::FindGraspPose_Response>()
{
  return auto_suture_interfaces::srv::builder::Init_FindGraspPose_Response_grasp_pose();
}

}  // namespace auto_suture_interfaces


namespace auto_suture_interfaces
{

namespace srv
{

namespace builder
{

class Init_FindGraspPose_Event_response
{
public:
  explicit Init_FindGraspPose_Event_response(::auto_suture_interfaces::srv::FindGraspPose_Event & msg)
  : msg_(msg)
  {}
  ::auto_suture_interfaces::srv::FindGraspPose_Event response(::auto_suture_interfaces::srv::FindGraspPose_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Event msg_;
};

class Init_FindGraspPose_Event_request
{
public:
  explicit Init_FindGraspPose_Event_request(::auto_suture_interfaces::srv::FindGraspPose_Event & msg)
  : msg_(msg)
  {}
  Init_FindGraspPose_Event_response request(::auto_suture_interfaces::srv::FindGraspPose_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_FindGraspPose_Event_response(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Event msg_;
};

class Init_FindGraspPose_Event_info
{
public:
  Init_FindGraspPose_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FindGraspPose_Event_request info(::auto_suture_interfaces::srv::FindGraspPose_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_FindGraspPose_Event_request(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPose_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::auto_suture_interfaces::srv::FindGraspPose_Event>()
{
  return auto_suture_interfaces::srv::builder::Init_FindGraspPose_Event_info();
}

}  // namespace auto_suture_interfaces

#endif  // AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSE__BUILDER_HPP_
