#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to auto_suture_interfaces__srv__FindGraspPosition_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FindGraspPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for FindGraspPosition_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FindGraspPosition_Request::default())
  }
}

impl rosidl_runtime_rs::Message for FindGraspPosition_Request {
  type RmwMsg = super::srv::rmw::FindGraspPosition_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to auto_suture_interfaces__srv__FindGraspPosition_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FindGraspPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_pose: geometry_msgs::msg::PoseStamped,

}



impl Default for FindGraspPosition_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FindGraspPosition_Response::default())
  }
}

impl rosidl_runtime_rs::Message for FindGraspPosition_Response {
  type RmwMsg = super::srv::rmw::FindGraspPosition_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.grasp_pose)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.grasp_pose)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      grasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.grasp_pose),
    }
  }
}






#[link(name = "auto_suture_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__auto_suture_interfaces__srv__FindGraspPosition() -> *const std::ffi::c_void;
}

// Corresponds to auto_suture_interfaces__srv__FindGraspPosition
#[allow(missing_docs, non_camel_case_types)]
pub struct FindGraspPosition;

impl rosidl_runtime_rs::Service for FindGraspPosition {
    type Request = FindGraspPosition_Request;
    type Response = FindGraspPosition_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__auto_suture_interfaces__srv__FindGraspPosition() }
    }
}


