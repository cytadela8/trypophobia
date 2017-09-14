#!/bin/bash

PATHek=$1

file $PATHek/* | grep -e HTML -e MP4 -e ASCII | cut -d":" -f1 | while read file; do
	rm $file
done
