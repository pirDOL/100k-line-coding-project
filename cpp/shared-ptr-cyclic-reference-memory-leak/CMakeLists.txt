cmake_minimum_required (VERSION 2.6)
project (main CXX)

set(CMAKE_C_COMPILER /opt/compiler/gcc-4.8.2/bin/gcc)
set(CMAKE_CXX_COMPILER /opt/compiler/gcc-4.8.2/bin/g++)

add_definitions(-g -Wall -pipe -fPIC -std=c++11 -DSHARED_PTR)
add_executable(main main.cpp)