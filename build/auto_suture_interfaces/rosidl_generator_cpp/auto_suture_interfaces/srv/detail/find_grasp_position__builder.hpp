// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from auto_suture_interfaces:srv/FindGraspPosition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "auto_suture_interfaces/srv/find_grasp_position.hpp"


#ifndef AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSITION__BUILDER_HPP_
#define AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSITION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "auto_suture_interfaces/srv/detail/find_grasp_position__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace auto_suture_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::auto_suture_interfaces::srv::FindGraspPosition_Request>()
{
  return ::auto_suture_interfaces::srv::FindGraspPosition_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace auto_suture_interfaces


namespace auto_suture_interfaces
{

namespace srv
{

namespace builder
{

class Init_FindGraspPosition_Response_grasp_pose
{
public:
  Init_FindGraspPosition_Response_grasp_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::auto_suture_interfaces::srv::FindGraspPosition_Response grasp_pose(::auto_suture_interfaces::srv::FindGraspPosition_Response::_grasp_pose_type arg)
  {
    msg_.grasp_pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPosition_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::auto_suture_interfaces::srv::FindGraspPosition_Response>()
{
  return auto_suture_interfaces::srv::builder::Init_FindGraspPosition_Response_grasp_pose();
}

}  // namespace auto_suture_interfaces


namespace auto_suture_interfaces
{

namespace srv
{

namespace builder
{

class Init_FindGraspPosition_Event_response
{
public:
  explicit Init_FindGraspPosition_Event_response(::auto_suture_interfaces::srv::FindGraspPosition_Event & msg)
  : msg_(msg)
  {}
  ::auto_suture_interfaces::srv::FindGraspPosition_Event response(::auto_suture_interfaces::srv::FindGraspPosition_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPosition_Event msg_;
};

class Init_FindGraspPosition_Event_request
{
public:
  explicit Init_FindGraspPosition_Event_request(::auto_suture_interfaces::srv::FindGraspPosition_Event & msg)
  : msg_(msg)
  {}
  Init_FindGraspPosition_Event_response request(::auto_suture_interfaces::srv::FindGraspPosition_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_FindGraspPosition_Event_response(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPosition_Event msg_;
};

class Init_FindGraspPosition_Event_info
{
public:
  Init_FindGraspPosition_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FindGraspPosition_Event_request info(::auto_suture_interfaces::srv::FindGraspPosition_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_FindGraspPosition_Event_request(msg_);
  }

private:
  ::auto_suture_interfaces::srv::FindGraspPosition_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::auto_suture_interfaces::srv::FindGraspPosition_Event>()
{
  return auto_suture_interfaces::srv::builder::Init_FindGraspPosition_Event_info();
}

}  // namespace auto_suture_interfaces

#endif  // AUTO_SUTURE_INTERFACES__SRV__DETAIL__FIND_GRASP_POSITION__BUILDER_HPP_
