cmake_minimum_required(VERSION 3.27)
project(SMAWS)

set(CMAKE_CXX_STANDARD 20)

add_subdirectory(lib/submodules/eigen)
add_subdirectory(lib/submodules/json)

include_directories(${PROJECT_SOURCE_DIR}/lib/submodules/eigen
                    ${PROJECT_SOURCE_DIR}/lib/submodules/json/include)

set(Library_Files
        lib/Server.cpp
        lib/Server.h
        lib/ScenarioSimulator.cpp
        lib/ScenarioSimulator.h
        lib/DatasetAPI.cpp
        lib/DatasetAPI.h
        lib/Dataset.h)

add_executable(${PROJECT_NAME} ${Library_Files} ipc.cpp) #main.cpp)
target_link_libraries(${PROJECT_NAME} PUBLIC eigen nlohmann_json::nlohmann_json)
