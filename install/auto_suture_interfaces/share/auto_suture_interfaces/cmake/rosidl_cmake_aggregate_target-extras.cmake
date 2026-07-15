# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target auto_suture_interfaces::auto_suture_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${auto_suture_interfaces_TARGETS}.
if(auto_suture_interfaces_TARGETS AND NOT TARGET auto_suture_interfaces::auto_suture_interfaces)
  add_library(auto_suture_interfaces::auto_suture_interfaces INTERFACE IMPORTED)
  set_target_properties(auto_suture_interfaces::auto_suture_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${auto_suture_interfaces_TARGETS}")
endif()
