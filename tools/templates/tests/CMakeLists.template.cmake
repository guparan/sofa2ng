#encoding utf-8
#compiler-settings
commentStartToken = //
cheetahVarStartToken = autopack::
#end compiler-settings
cmake_minimum_required(VERSION 3.1)
project(autopack::package_name_test VERSION 1.0)

#for depend in autopack::dependencies_test
find_package(autopack::depend)
#end for

set(HEADER_FILES
#for filename in autopack::header_files
    autopack::filename
#end for
)

set(SOURCE_FILES
#for filename in autopack::source_files
    autopack::filename
#end for
)

add_executable(${PROJECT_NAME} ${HEADER_FILES} ${SOURCE_FILES} ${EXTRA_FILES})
target_link_libraries(${PROJECT_NAME} PUBLIC autopack::{sorted_dependencies_test} )

add_test(NAME ${PROJECT_NAME} COMMAND ${PROJECT_NAME})
