cmake_minimum_required(VERSION 3.10)
project(HelloVitals)

set(CMAKE_CXX_STANDARD 17)

# Find OpenCV
find_package(OpenCV REQUIRED)

# Find GLog
find_package(glog REQUIRED)

# If the SmartSpectra SDK is installed in a specific directory, set it here
# set(SmartSpectra_DIR "/path/to/sdk")

add_executable(hello_vitals hello_vitals.cpp)

# Link necessary libraries
target_link_libraries(hello_vitals 
    PRIVATE 
    ${OpenCV_LIBS} 
    glog::glog
    # Replace these with the actual Presage SDK library names provided in your SDK folder
    smartspectra_container
    smartspectra_gui
    physiology_messages
)

target_include_directories(hello_vitals PRIVATE 
    ${OpenCV_INCLUDE_DIRS}
    # Add the path to your Presage SDK include folder
    "/usr/local/include/presage" 
)