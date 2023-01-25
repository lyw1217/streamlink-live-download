#!/bin/bash

VIDEO_PATH="/volume2/streamlink/mnt/recordings/uploaded"
PERIOD=2592000  # 30 days (seconds)

if [ ! -d ${VIDEO_PATH} ]; then
    echo "'${VIDEO_PATH}' Directory does not exist!"
    echo "exit"
    exit
fi

delete_old() {
	for arg in "$1"/*
	do
		if [ ! -e "$arg" ]; then
			echo "File "$arg" is not exists."
			continue
		fi

		if [ -d "$arg" ]; then
			echo "directory ${arg}"
			delete_old $arg
			continue
		fi

        time_close=`stat -c %Y $arg`
        time_now=`date +%s`
        time_diff=`expr $time_now - $time_close`
        if [ $time_diff -gt $PERIOD ]; then
            rm -f $arg
        fi
    done
}

delete_old $VIDEO_PATH