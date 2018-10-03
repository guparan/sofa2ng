#!/bin/bash

usage() {
    echo "Usage: deploy.sh <recipe_name> [-s,--simulate]"
    echo "-s, --simulate: no file removal"
    echo "Info: deploy.sh directory must be in sofa_src/tools"
}

parse_args() {
    case "$1" in
        -s|--simulate)
            simulate="true"
            ;;
        *)
            recipe="$1"
            ;;
    esac
}

simulate="false"
while [[ "$#" -ge 1 ]]; do
    parse_args "$1"
    shift
done
    
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
pwd

py -2 ./tools/bootstrap.py "$simulate" "$recipe" "../.." "../../modules"
