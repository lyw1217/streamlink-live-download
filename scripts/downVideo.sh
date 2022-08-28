#!/bin/bash

# 하루 전 영상을 다운로드받는 스크립트

VIDEO_PATH="${HOME}/mnt/Twitch/recordings"
INPUT="${HOME}/Documents/github/streamlink-live-download/download_url.txt"
TARGET_URLS=()
PROGRAM="yt-dlp"
CMD=`command -v ${PROGRAM} 2>/dev/null`

if [ ! -d ${VIDEO_PATH} ]; then
    echo "'${VIDEO_PATH}' Directory does not exist!"
    echo "exit"
    exit
fi

if [ ! -e ${INPUT} ]; then
    echo "'${INPUT}' File does not exist!"
    echo "exit"
    exit
fi

if [ -z "$CMD" ]; then
    echo "${PROGRAM} command does not exist!"
    echo "Please, Install youtube-dl. refer to https://github.com/ytdl-org/youtube-dl/blob/master/README.md#installation"
    echo "exit"
    exit
fi 

echo "===START DOWNLOAD SCRIPT==="

while read url; do
    if [ -z "$url" ]; then continue; fi
    TARGET_URLS+=($url)
done < $INPUT

echo "TARGET_URLS = ${TARGET_URLS}"

for arg in "${TARGET_URLS[@]}"
do
    echo ""
    echo "download start!!!"
	echo $arg
    
	$CMD --verbose -f bestvideo*+bestaudio/best --throttled-rate 100k --playlist-end 5 --dateafter now-1day -o "${VIDEO_PATH}/[%(uploader)s]_%(upload_date)s_%(title)s.%(ext)s" "${arg}/videos"
    
    echo "download complete!!!"
    echo ""
    sleep 5
done

echo "=== END  DOWNLOAD SCRIPT==="
