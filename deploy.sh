#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR

# py -2 ./tools/mc.py recipes/Sofa.Component.Utils.rcpy ../.. ../../modules
py -2 ./tools/mc.py recipes/Sofa.Helper.Bvh.rcpy ../.. ../../modules
