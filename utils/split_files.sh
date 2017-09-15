#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 source target count"
    exit
fi

SOURCE=$1
TARGET=$2
COUNT=$3

find $SOURCE -type f | shuf | head -n $COUNT | while read -r file; do
	mv "$file" "$TARGET"
done
