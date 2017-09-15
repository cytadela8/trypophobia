#!/bin/bash

# For every .gif file in every subfolder of a given folder this script checks the number of frames (If the gif is animated) and outputs that information.

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 source PATH"
    exit
fi

PATH=$1

shopt -s globstar
for i in $PATH/**/*.gif; do
  if [ `identify "$i" | wc -l` -gt 1 ] ; then
    echo animated: "$i"
  else
    echo one frame: "$i"
  fi
done
