#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR


# ./tools/mc.py recipes/bootstrap-migration.rcpy ../.. ../..
# ./tools/mc.py recipes/Sofa.Config/Sofa.Config.rcpy ../.. ../../kernel
#./tools/mc.py recipes/Sofa.Type/Sofa.Type.rcpy ../.. ng/kernel
py -2 ./tools/mc.py recipes/Sofa.Component.Utils.rcpy ../.. ../../modules
# py -2 ./tools/mc.py recipes/Sofa.Helper.Bvh.rcpy ../.. ../../modules

# #### Prepare kernel
# echo "cmake_minimum_required(VERSION 3.5)" > ../../kernel/CMakeLists.txt
# echo 'set(CMAKE_PREFIX_PATH "${CMAKE_BINARY_DIR}/cmake")' >> ../../kernel/CMakeLists.txt
# echo 'set(CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}/cmake")' >> ../../kernel/CMakeLists.txt
# echo "add_subdirectory(Sofa.Config)" >> ../../kernel/CMakeLists.txt
# echo "add_subdirectory(Sofa.Config/tests)" >> ../../kernel/CMakeLists.txt

# #### Prepare modules
# echo "cmake_minimum_required(VERSION 3.5)" > ../../modules/CMakeLists.txt
# echo 'set(CMAKE_PREFIX_PATH "${CMAKE_BINARY_DIR}/cmake")' >> ../../modules/CMakeLists.txt
# echo 'set(CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}/cmake")' >> ../../modules/CMakeLists.txt
# echo "add_subdirectory(Sofa.Component.Utils)" >> ../../modules/CMakeLists.txt
