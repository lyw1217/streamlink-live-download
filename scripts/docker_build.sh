#!/bin/bash

DOCKER=`which docker`

if [ $# -lt 2 ] ; then
    echo "Usage : $0 [image name] [tag]"
    echo
	echo "--Docker Images--"
	$DOCKER images
    exit 0
fi

#DOCKER build -t $1:$2 ../
$DOCKER buildx build --push --platform linux/arm64,linux/amd64 --tag $1:$2 "../"
