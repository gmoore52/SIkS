cmake_minimum_required(VERSION 3.27)
project(SMAWS)

set(CMAKE_CXX_STANDARD 20)

set(Library_Files
        lib/ScenarioSimulator.cpp
        lib/ScenarioSimulator.h)

add_executable(${PROJECT_NAME} ${Library_Files} main.cpp)
