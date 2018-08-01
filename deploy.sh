#!/bin/bash

usage() {
    echo "Usage: deploy.sh <recipe_name>"
    echo "Info: deploy.sh directory must be in sofa_src/tools"
}

if [ "$#" -eq 1 ]; then
    recipe="$1"
else
    usage; exit 1
fi    
    
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
pwd

py -2 ./tools/bootstrap.py $recipe ../.. ../../modules
