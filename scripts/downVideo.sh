#!/bin/bash
VIDEO_PATH="${HOME}/mnt/Twitch/recordings"
TARGET_URLS=()
PROGRAM="youtube-dl"
CMD=`command -v ${PROGRAM} 2>/dev/null`

if [ ! -d ${VIDEO_PATH} ]; then
    echo "'${VIDEO_PATH}' Directory does not exist!"
    echo "exit"
    exit
fi

if [ -z "$CMD" ]; then
    echo "${PROGRAM} command does not exist!"
    echo "Please, Install youtube-dl. refer to https://github.com/ytdl-org/youtube-dl/blob/master/README.md#installation"
    echo "exit"
    exit
fi 

while read url; do
    if [ -z "$url" ]; then continue; fi
    TARGET_URLS+=($url)
done < /home/ubuntu/Documents/github/streamlink-live-download/download_url.txt

for arg in "${TARGET_URLS[@]}"
do
    echo ""
    echo "download start!!!"
	echo $arg
    
	$CMD -g -f bestvideo+bestaudio/best --limit-rate 8M --playlist-end 5 --buffer-size 16K --dateafter now-1day -o "${VIDEO_PATH}/%(uploader)s %(upload_date)s %(title)s.%(ext)s" "${arg}/videos"
    
    echo "download complete!!!"
    echo ""
    sleep 5
done

