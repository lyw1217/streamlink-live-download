#!/bin/bash

# 영상의 길이를 구하는 스크립트 

#if [ $# -eq 0 ]; then
#	echo "No arguments supplied"
#fi
VIDEO_PATH="${HOME}/mnt/Twitch/recordings"
PROGRAM="ffprobe"
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

get_duration() {
	for arg in "$1"/*
	do
		if [ ! -e "$arg" ]; then
			echo "File "$arg" is not exists."
			continue
		fi

		if [ -d "$arg" ]; then
			echo "directory ${arg}"
			get_duration $arg
			continue
		fi
		
		fileext=${arg##*.}
		if [ "$fileext" == "txt" ]; then
			continue
		fi
		
		echo $arg

		$CMD -i "${arg}" 2>&1 | grep Duration | awk '{print $2}' | tr -d ,

		echo

	done
}

get_duration $VIDEO_PATH