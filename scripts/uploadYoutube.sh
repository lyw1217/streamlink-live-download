#!/bin/bash

# 유튜브 업로드 스크립트

#if [ $# -eq 0 ]; then
#	echo "No arguments supplied"
#fi
VIDEO_PATH="${HOME}/mnt/Twitch/recordings/saved"

# 가상 환경 진입
. ${HOME}/Documents/github/streamlink-live-download/venv/bin/activate

PROGRAM="python"
CMD=`command -v ${PROGRAM} 2>/dev/null`
UPLOAD_PY="${HOME}/Documents/github/streamlink-live-download/src/upload_youtube.py"

if [ ! -d ${VIDEO_PATH} ]; then
    echo "'${VIDEO_PATH}' Directory does not exist!"
    echo "exit"
    exit
fi

if [ -z "$CMD" ]; then
    echo "${PROGRAM} command does not exist!"
    echo "exit"
    exit
fi 

upload_youtube() {
	for arg in "$1"/*
	do
		if [ ! -e "$arg" ]; then
			echo "File "$arg" is not exists."
			continue
		fi

		if [ -d "$arg" ]; then
			echo "directory ${arg}"
			upload_youtube $arg
			continue
		fi
		
		fileext=${arg##*.}
		if [ "$fileext" == "m2ts" ] || [ "$fileext" == "ts" ] || [ "$fileext" == "mp4" ] ; then
			echo "uploading file ${arg}...!"
			FILE=`basename -s .${fileext} ${arg}`
			# https://m.blog.naver.com/oasiss12/221600130084
			FILE_NAME="$( echo "${FILE}" |  tr '\12' ' ' )"
			$CMD $UPLOAD_PY --file "${arg}" --description "${FILE_NAME}" --category 24 --title "${FILE_NAME}" --privacyStatus private #--noauth_local_webserver
			echo "upload complete file ${arg}"
		fi
		echo
	done
}

upload_youtube $VIDEO_PATH
