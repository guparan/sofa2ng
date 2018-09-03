#encoding utf-8
#compiler-settings
commentStartToken = //
cheetahVarStartToken = autopack::
#end compiler-settings
#set autopack::test_dependencies_str = ' '.join(sorted(autopack::test_dependencies))
cmake_minimum_required(VERSION 3.1)

project(autopack::{package_name}.test VERSION 1.0)

#for depend in sorted(autopack::test_dependency_targets)
find_package(autopack::depend)
#end for

set(HEADER_FILES
#for filename in sorted(autopack::test_header_files)
    autopack::filename
#end for
)

set(SOURCE_FILES
#for filename in sorted(autopack::test_source_files)
    autopack::filename
#end for
)

add_executable(${PROJECT_NAME} ${HEADER_FILES} ${SOURCE_FILES} ${EXTRA_FILES})
target_link_libraries(${PROJECT_NAME} PUBLIC autopack::{test_dependencies_str})

add_test(NAME ${PROJECT_NAME} COMMAND ${PROJECT_NAME})
