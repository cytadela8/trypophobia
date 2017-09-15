#!/bin/bash

# This script takes one folder as arguments and renames all files in subdirectories of that folder to ORYGINAL_NAME.MD5_SUM.EXTENSION

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PATH"
    exit
fi

PATHek=$1

shopt -s globstar

for file in $PATHek/**/*; do
	extension="${file##*.}"                     # get the extension
	filename="${file%.*}"                       # get the filename
	mv "$file" "${filename}-$(md5sum $file | cut -d " " -f 1).${extension}"
	printf "."
done



