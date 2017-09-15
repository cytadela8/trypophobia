#!/bin/bash

# This script downloads async all files from neptune folder. (It will probably be unnecessery in near future)
# WARNING: this scripts exits before everything is downloaded and it may use A LOT OF RAM

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /experiments/<uuid>/jobs/<uuid>/output/"
    exit
fi


FOLDER=$1

neptune data ls "$FOLDER" | cut -d $'\t' -f 4 | while read -r file; do 
	echo $file
	neptune data download "$FOLDER$file" &
done
echo Uruchomiono wszystkie watki
