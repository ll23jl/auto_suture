#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "auto_suture_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__auto_suture_interfaces__srv__FindGraspPose_Request() -> *const std::ffi::c_void;
}

#[link(name = "auto_suture_interfaces__rosidl_generator_c")]
extern "C" {
    fn auto_suture_interfaces__srv__FindGraspPose_Request__init(msg: *mut FindGraspPose_Request) -> bool;
    fn auto_suture_interfaces__srv__FindGraspPose_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<FindGraspPose_Request>, size: usize) -> bool;
    fn auto_suture_interfaces__srv__FindGraspPose_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<FindGraspPose_Request>);
    fn auto_suture_interfaces__srv__FindGraspPose_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<FindGraspPose_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<FindGraspPose_Request>) -> bool;
}

// Corresponds to auto_suture_interfaces__srv__FindGraspPose_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FindGraspPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub psm: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_type: rosidl_runtime_rs::String,

}



impl Default for FindGraspPose_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !auto_suture_interfaces__srv__FindGraspPose_Request__init(&mut msg as *mut _) {
        panic!("Call to auto_suture_interfaces__srv__FindGraspPose_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for FindGraspPose_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { auto_suture_interfaces__srv__FindGraspPose_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { auto_suture_interfaces__srv__FindGraspPose_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { auto_suture_interfaces__srv__FindGraspPose_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for FindGraspPose_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for FindGraspPose_Request where Self: Sized {
  const TYPE_NAME: &'static str = "auto_suture_interfaces/srv/FindGraspPose_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__auto_suture_interfaces__srv__FindGraspPose_Request() }
  }
}


#[link(name = "auto_suture_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__auto_suture_interfaces__srv__FindGraspPose_Response() -> *const std::ffi::c_void;
}

#[link(name = "auto_suture_interfaces__rosidl_generator_c")]
extern "C" {
    fn auto_suture_interfaces__srv__FindGraspPose_Response__init(msg: *mut FindGraspPose_Response) -> bool;
    fn auto_suture_interfaces__srv__FindGraspPose_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<FindGraspPose_Response>, size: usize) -> bool;
    fn auto_suture_interfaces__srv__FindGraspPose_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<FindGraspPose_Response>);
    fn auto_suture_interfaces__srv__FindGraspPose_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<FindGraspPose_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<FindGraspPose_Response>) -> bool;
}

// Corresponds to auto_suture_interfaces__srv__FindGraspPose_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FindGraspPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for FindGraspPose_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !auto_suture_interfaces__srv__FindGraspPose_Response__init(&mut msg as *mut _) {
        panic!("Call to auto_suture_interfaces__srv__FindGraspPose_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for FindGraspPose_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { auto_suture_interfaces__srv__FindGraspPose_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { auto_suture_interfaces__srv__FindGraspPose_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { auto_suture_interfaces__srv__FindGraspPose_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for FindGraspPose_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for FindGraspPose_Response where Self: Sized {
  const TYPE_NAME: &'static str = "auto_suture_interfaces/srv/FindGraspPose_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__auto_suture_interfaces__srv__FindGraspPose_Response() }
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


