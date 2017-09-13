#!/bin/bash

FOLDER=$1

neptune data ls "$FOLDER" | cut -d $'\t' -f 4 | while read -r file; do 
	echo $file
	neptune data download "$FOLDER$file" &
done
echo Uruchomiono wszystkie watki
