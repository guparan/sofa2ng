#encoding utf-8
#compiler-settings
commentStartToken = //
cheetahVarStartToken = autopack::
#end compiler-settings
#set autopack::dependencies_str = ' '.join(autopack::dependencies)
cmake_minimum_required(VERSION 3.1)

project(autopack::package_name VERSION 1.0)

#for depend in autopack::dependency_targets
find_package(autopack::depend)
#end for

set(HEADER_FILES config/${PROJECT_NAME}.h)
set(SOURCE_FILES config/${PROJECT_NAME}.cpp)

list(APPEND HEADER_FILES
#for filename in autopack::deprecated_header_files   
    autopack::filename
#end for
)

list(APPEND HEADER_FILES
#for filename in autopack::header_files   
    autopack::filename
#end for
)
list(APPEND SOURCE_FILES
#for filename in autopack::source_files 
    autopack::filename
#end for
)

set(EXTRA_FILES
#for filename in autopack::extra_files
    autopack::filename
#end for
)

#if autopack::package_type == "executable"
add_autopack::{package_type}(${PROJECT_NAME} ${HEADER_FILES} ${SOURCE_FILES} ${EXTRA_FILES})
#else
add_autopack::{package_type}(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${EXTRA_FILES})
#end if
target_link_libraries(${PROJECT_NAME} PUBLIC autopack::{dependencies_str})
target_compile_definitions(${PROJECT_NAME} PRIVATE "-DBUILD_autopack::package_cname")
target_include_directories(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/config>")
target_include_directories(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/deprecated_layout>")
target_include_directories(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src>")

sofa_create_package(${PROJECT_NAME} ${PROJECT_VERSION} ${PROJECT_NAME} ${PROJECT_NAME})
