cmake_minimum_required (VERSION 2.6)
project (app CXX)

add_definitions(-g -Wall -pipe -fPIC)

add_library(app SHARED app.cpp)
target_include_directories(app PUBLIC ../log)
#find_library(liblog_path log_a ../log)
find_library(liblog_path log_so ../log)
target_link_libraries(app ${liblog_path})
message(STATUS "liblog_path: " ${liblog_path})
