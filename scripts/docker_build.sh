#!/bin/bash

DOCKER=`which docker`

if [ $# -lt 2 ] ; then
    echo "Usage : $0 {TAG} {VERSION}"
    exit 0
fi

$DOCKER build -t $1:$2 ../