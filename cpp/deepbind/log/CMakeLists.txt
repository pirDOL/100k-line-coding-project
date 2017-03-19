cmake_minimum_required (VERSION 2.6)
project (so_static CXX)

add_definitions(-g -Wall -pipe -fPIC)

add_library(log_a STATIC log.cpp)
add_library(log_so SHARED log.cpp)
