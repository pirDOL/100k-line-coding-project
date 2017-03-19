cmake_minimum_required (VERSION 2.6)
project (frame CXX)

add_definitions(-g -Wall -pipe -fPIC)

add_executable(frame frame.cpp)
target_include_directories(frame PUBLIC ../log)
#find_library(liblog_path log_a ../log)
find_library(liblog_path log_so ../log)
target_link_libraries(frame ${liblog_path} dl)
message(STATUS "liblog_path: " ${liblog_path})
