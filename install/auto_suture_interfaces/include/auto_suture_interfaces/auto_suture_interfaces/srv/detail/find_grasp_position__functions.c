// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from auto_suture_interfaces:srv/FindGraspPosition.idl
// generated code does not contain a copyright notice
#include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
auto_suture_interfaces__srv__FindGraspPosition_Request__init(auto_suture_interfaces__srv__FindGraspPosition_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Request__fini(auto_suture_interfaces__srv__FindGraspPosition_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Request__are_equal(const auto_suture_interfaces__srv__FindGraspPosition_Request * lhs, const auto_suture_interfaces__srv__FindGraspPosition_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Request__copy(
  const auto_suture_interfaces__srv__FindGraspPosition_Request * input,
  auto_suture_interfaces__srv__FindGraspPosition_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

auto_suture_interfaces__srv__FindGraspPosition_Request *
auto_suture_interfaces__srv__FindGraspPosition_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Request * msg = (auto_suture_interfaces__srv__FindGraspPosition_Request *)allocator.allocate(sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request));
  bool success = auto_suture_interfaces__srv__FindGraspPosition_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Request__destroy(auto_suture_interfaces__srv__FindGraspPosition_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    auto_suture_interfaces__srv__FindGraspPosition_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__init(auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request)) {
      return false;
    }
    data = (auto_suture_interfaces__srv__FindGraspPosition_Request *)allocator.zero_allocate(size, sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = auto_suture_interfaces__srv__FindGraspPosition_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        auto_suture_interfaces__srv__FindGraspPosition_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__fini(auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      auto_suture_interfaces__srv__FindGraspPosition_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence *
auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * array = (auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence *)allocator.allocate(sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__destroy(auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__are_equal(const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * lhs, const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!auto_suture_interfaces__srv__FindGraspPosition_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__copy(
  const auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * input,
  auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(auto_suture_interfaces__srv__FindGraspPosition_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    auto_suture_interfaces__srv__FindGraspPosition_Request * data =
      (auto_suture_interfaces__srv__FindGraspPosition_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!auto_suture_interfaces__srv__FindGraspPosition_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          auto_suture_interfaces__srv__FindGraspPosition_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!auto_suture_interfaces__srv__FindGraspPosition_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `grasp_pose`
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"

bool
auto_suture_interfaces__srv__FindGraspPosition_Response__init(auto_suture_interfaces__srv__FindGraspPosition_Response * msg)
{
  if (!msg) {
    return false;
  }
  // grasp_pose
  if (!geometry_msgs__msg__PoseStamped__init(&msg->grasp_pose)) {
    auto_suture_interfaces__srv__FindGraspPosition_Response__fini(msg);
    return false;
  }
  return true;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Response__fini(auto_suture_interfaces__srv__FindGraspPosition_Response * msg)
{
  if (!msg) {
    return;
  }
  // grasp_pose
  geometry_msgs__msg__PoseStamped__fini(&msg->grasp_pose);
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Response__are_equal(const auto_suture_interfaces__srv__FindGraspPosition_Response * lhs, const auto_suture_interfaces__srv__FindGraspPosition_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // grasp_pose
  if (!geometry_msgs__msg__PoseStamped__are_equal(
      &(lhs->grasp_pose), &(rhs->grasp_pose)))
  {
    return false;
  }
  return true;
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Response__copy(
  const auto_suture_interfaces__srv__FindGraspPosition_Response * input,
  auto_suture_interfaces__srv__FindGraspPosition_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // grasp_pose
  if (!geometry_msgs__msg__PoseStamped__copy(
      &(input->grasp_pose), &(output->grasp_pose)))
  {
    return false;
  }
  return true;
}

auto_suture_interfaces__srv__FindGraspPosition_Response *
auto_suture_interfaces__srv__FindGraspPosition_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Response * msg = (auto_suture_interfaces__srv__FindGraspPosition_Response *)allocator.allocate(sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response));
  bool success = auto_suture_interfaces__srv__FindGraspPosition_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Response__destroy(auto_suture_interfaces__srv__FindGraspPosition_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    auto_suture_interfaces__srv__FindGraspPosition_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__init(auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response)) {
      return false;
    }
    data = (auto_suture_interfaces__srv__FindGraspPosition_Response *)allocator.zero_allocate(size, sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = auto_suture_interfaces__srv__FindGraspPosition_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        auto_suture_interfaces__srv__FindGraspPosition_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__fini(auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      auto_suture_interfaces__srv__FindGraspPosition_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence *
auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * array = (auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence *)allocator.allocate(sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__destroy(auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__are_equal(const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * lhs, const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!auto_suture_interfaces__srv__FindGraspPosition_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__copy(
  const auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * input,
  auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(auto_suture_interfaces__srv__FindGraspPosition_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    auto_suture_interfaces__srv__FindGraspPosition_Response * data =
      (auto_suture_interfaces__srv__FindGraspPosition_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!auto_suture_interfaces__srv__FindGraspPosition_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          auto_suture_interfaces__srv__FindGraspPosition_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!auto_suture_interfaces__srv__FindGraspPosition_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "auto_suture_interfaces/srv/detail/find_grasp_position__functions.h"

bool
auto_suture_interfaces__srv__FindGraspPosition_Event__init(auto_suture_interfaces__srv__FindGraspPosition_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    auto_suture_interfaces__srv__FindGraspPosition_Event__fini(msg);
    return false;
  }
  // request
  if (!auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__init(&msg->request, 0)) {
    auto_suture_interfaces__srv__FindGraspPosition_Event__fini(msg);
    return false;
  }
  // response
  if (!auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__init(&msg->response, 0)) {
    auto_suture_interfaces__srv__FindGraspPosition_Event__fini(msg);
    return false;
  }
  return true;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Event__fini(auto_suture_interfaces__srv__FindGraspPosition_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__fini(&msg->request);
  // response
  auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__fini(&msg->response);
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Event__are_equal(const auto_suture_interfaces__srv__FindGraspPosition_Event * lhs, const auto_suture_interfaces__srv__FindGraspPosition_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Event__copy(
  const auto_suture_interfaces__srv__FindGraspPosition_Event * input,
  auto_suture_interfaces__srv__FindGraspPosition_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!auto_suture_interfaces__srv__FindGraspPosition_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!auto_suture_interfaces__srv__FindGraspPosition_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

auto_suture_interfaces__srv__FindGraspPosition_Event *
auto_suture_interfaces__srv__FindGraspPosition_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Event * msg = (auto_suture_interfaces__srv__FindGraspPosition_Event *)allocator.allocate(sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event));
  bool success = auto_suture_interfaces__srv__FindGraspPosition_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Event__destroy(auto_suture_interfaces__srv__FindGraspPosition_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    auto_suture_interfaces__srv__FindGraspPosition_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__init(auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event)) {
      return false;
    }
    data = (auto_suture_interfaces__srv__FindGraspPosition_Event *)allocator.zero_allocate(size, sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = auto_suture_interfaces__srv__FindGraspPosition_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        auto_suture_interfaces__srv__FindGraspPosition_Event__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__fini(auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      auto_suture_interfaces__srv__FindGraspPosition_Event__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence *
auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * array = (auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence *)allocator.allocate(sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__destroy(auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__are_equal(const auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * lhs, const auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!auto_suture_interfaces__srv__FindGraspPosition_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence__copy(
  const auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * input,
  auto_suture_interfaces__srv__FindGraspPosition_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(auto_suture_interfaces__srv__FindGraspPosition_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    auto_suture_interfaces__srv__FindGraspPosition_Event * data =
      (auto_suture_interfaces__srv__FindGraspPosition_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!auto_suture_interfaces__srv__FindGraspPosition_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          auto_suture_interfaces__srv__FindGraspPosition_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!auto_suture_interfaces__srv__FindGraspPosition_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
