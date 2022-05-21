cmake_minimum_required(VERSION 3.20)
project(graphics-net-transfers)

set(CMAKE_C_COMPILER gcc)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_STANDARD 20)


add_executable(main src/main.cpp)
