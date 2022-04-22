#!/bin/bash
VIDEO_PATH="${HOME}/mnt/Twitch/recordings"
TARGET_URLS=()

while read url; do
    if [ -z "$url" ]; then continue; fi
    TARGET_URLS+=($url)
done < /home/ubuntu/Documents/github/streamlink-live-download/download_url.txt

for arg in "${TARGET_URLS[@]}"
do
    echo ""
    echo "download start!!!"
	echo $arg
    
	youtube-dl -f bestvideo+bestaudio/best --limit-rate 8M --playlist-end 1 --buffer-size 16K --dateafter now-1day -o "${VIDEO_PATH}/%(uploader)s %(upload_date)s %(title)s.%(ext)s" "${arg}/videos"
    
    echo "download complete!!!"
    echo ""
    sleep 5
done

