cmake_minimum_required(VERSION 3.16)
project(pi_driver)

message("Starting build process")

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Check that BCM2835 library was properly installed
set(BCM_DRIVER_VERSION 1.68)
set(BCM_DRIVER_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../bcm2835-${BCM_DRIVER_VERSION})
if(NOT EXISTS ${BCM_DRIVER_PATH})
  message(
    FATAL_ERROR
      "BCM2835-${BCM_DRIVER_VERSION} is not installed in ${BCM_DRIVER_PATH}")
endif()
message("Found BCM2835-${BCM_DRIVER_VERSION} library at ${BCM_DRIVER_PATH}")

# Include and link BCM2835 dependencies for GPIO control using Raspberry Pi 4
include_directories(include ${BCM_DRIVER_PATH}/src)
message(${BCM_DRIVER_PATH}/src)
link_libraries(${BCM_DRIVER_PATH}/src/bcm2835.o)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(pi_driver src/pi_driver.cpp)
ament_target_dependencies(pi_driver rclcpp std_msgs)

target_link_libraries(pi_driver bcm2835)

install(TARGETS
  pi_driver
  DESTINATION lib/${PROJECT_NAME})

ament_package()