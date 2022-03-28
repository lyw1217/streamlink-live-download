#!/bin/bash

#if [ $# -eq 0 ]; then
#	echo "No arguments supplied"
#fi
VIDEO_PATH="/home/leeyw/mnt/Twitch/recordings"
#for arg in "$@"
for arg in "$VIDEO_PATH"/*
do
	if [ ! -e "$arg" ]; then
		echo "File "$arg" is not exists."
		continue
	fi
	
	fileext=${arg##*.}
	if [ "$fileext" != "ts" ]; then
		continue
	fi
	
	echo $arg

	ffmpeg -i $arg 2>&1 | grep Duration | awk '{print $2}' | tr -d ,

	echo

	sleep 5
done
