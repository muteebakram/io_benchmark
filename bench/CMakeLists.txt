cmake_minimum_required(VERSION 3.10)
project(IOBench)

set(CMAKE_CXX_STANDARD 23)

find_package(OpenSSL REQUIRED)

add_executable(bench bench.cpp)
target_link_libraries(bench OpenSSL::SSL)
