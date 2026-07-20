#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to auto_suture_interfaces__srv__FindGraspPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FindGraspPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub psm: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_type: std::string::String,

}



impl Default for FindGraspPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FindGraspPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for FindGraspPose_Request {
  type RmwMsg = super::srv::rmw::FindGraspPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        psm: msg.psm.as_str().into(),
        grasp_type: msg.grasp_type.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        psm: msg.psm.as_str().into(),
        grasp_type: msg.grasp_type.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      psm: msg.psm.to_string(),
      grasp_type: msg.grasp_type.to_string(),
    }
  }
}


// Corresponds to auto_suture_interfaces__srv__FindGraspPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FindGraspPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub approach_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for FindGraspPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FindGraspPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for FindGraspPose_Response {
  type RmwMsg = super::srv::rmw::FindGraspPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.grasp_pose)).into_owned(),
        approach_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.approach_pose)).into_owned(),
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.grasp_pose)).into_owned(),
        approach_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.approach_pose)).into_owned(),
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      grasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.grasp_pose),
      approach_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.approach_pose),
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "auto_suture_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__auto_suture_interfaces__srv__FindGraspPose() -> *const std::ffi::c_void;
}

// Corresponds to auto_suture_interfaces__srv__FindGraspPose
#[allow(missing_docs, non_camel_case_types)]
pub struct FindGraspPose;

impl rosidl_runtime_rs::Service for FindGraspPose {
    type Request = FindGraspPose_Request;
    type Response = FindGraspPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__auto_suture_interfaces__srv__FindGraspPose() }
    }
}


