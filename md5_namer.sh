#!/bin/bash

PATHek=$1

shopt -s globstar

for file in $PATHek/**/*; do
	extension="${file##*.}"                     # get the extension
	filename="${file%.*}"                       # get the filename
	mv "$file" "${filename}-$(md5sum $file | cut -d " " -f 1).${extension}"
	printf "."
done



