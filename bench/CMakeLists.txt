cmake_minimum_required(VERSION 3.10)
project(IOBench)

set(CMAKE_CXX_STANDARD 23)

include(FetchContent)
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)

find_package(OpenSSL REQUIRED)
add_executable(bench bench.cpp)
target_link_libraries(bench PRIVATE nlohmann_json::nlohmann_json OpenSSL::SSL uring)
