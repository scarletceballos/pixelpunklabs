#!/bin/bash

# Path to Blender executable on Mac
BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"

# Run Blender in background mode with your Python script
"$BLENDER_PATH" --background --python blender_api.py 