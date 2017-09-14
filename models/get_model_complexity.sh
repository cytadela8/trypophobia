#!/usr/bin/env bash

#Usage: ./get_model_complexity.sh [path_to_main.py_of_the_model]

tail -n +$(nl $1 | grep "import common" | awk '{print $1+1}') $1 | sed '/common.experiment(.*)/ s/)/.summary()/' | sed 's/^common.experiment(//' | sed 's/common.resolution_./256/g' | python3 2>&1 | grep params
