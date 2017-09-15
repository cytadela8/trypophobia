#!/bin/bash

# For every file in folder this script checks if it's a HTML, MP4 or ASCII files and if so removes it

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PATH"
    exit
fi


PATHek=$1

file $PATHek/* | grep -e HTML -e MP4 -e ASCII | cut -d":" -f1 | while read file; do
	rm $file
done
