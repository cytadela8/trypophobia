#!/usr/bin/env bash

# This script reports number of parameter in model defined in .py script with path

if [ "$#" -ne 1 ]; then
    echo Usage: $0 path_to_main.py_of_the_model
    exit
fi


tail -n +$(nl $1 | grep "import common" | awk '{print $1+1}') $1 | sed '/common.experiment(.*)/ s/)/.summary()/' | sed 's/^common.experiment(//' | sed 's/common.resolution_./256/g' | python3 2>&1 | grep params
