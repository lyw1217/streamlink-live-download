#!/bin/bash

source ./venv/bin/activate

PROGRAM="python"
CMD=`command -v ${PROGRAM} 2>/dev/null`

$CMD ./src/main.py