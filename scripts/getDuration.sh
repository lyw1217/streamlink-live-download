#!/bin/bash

#if [ $# -eq 0 ]; then
#	echo "No arguments supplied"
#fi
VIDEO_PATH="${HOME}/mnt/Twitch/recordings"
PROGRAM="ffmpeg"
CMD=`command -v ${PROGRAM} 2>/dev/null`

if [ ! -d ${VIDEO_PATH} ]; then
    echo "'${VIDEO_PATH}' Directory does not exist!"
    echo "exit"
    exit
fi

if [ -z "$CMD" ]; then
    echo "${PROGRAM} command does not exist!"
    echo "Please, Install ffmpeg. refer to https://ffmpeg.org/download.html"
    echo "exit"
    exit
fi 

#for arg in "$@"
for arg in "$VIDEO_PATH"/*
do
	if [ ! -e "$arg" ]; then
		echo "File "$arg" is not exists."
		continue
	fi
	
	fileext=${arg##*.}
	if [ "$fileext" == "txt" ]; then
		continue
	fi
	
	echo $arg

	ffmpeg -i $arg 2>&1 | grep Duration | awk '{print $2}' | tr -d ,

	echo

done

sleep 5
