#!/bin/bash

# Check if two arguments were provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 SOURCE_DIR DEST_DIR"
    exit 1
fi

# Assign arguments to variables
SOURCE_DIR="$1"
DEST_DIR="$2"

# Use fswatch to monitor the directory and trigger rsync
fswatch -o "$SOURCE_DIR" | while read f; do
  rsync -avz --delete --exclude 'venv_pi/' -e ssh $SOURCE_DIR $DEST_DIR
done
