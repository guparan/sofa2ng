#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR

module="$1"

py -2 ./tools/mc.py recipes/$module.rcpy ../.. ../../modules
