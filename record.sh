#!/bin/bash

ROOT_DIR="${HOME}/Documents/github/streamlink-live-download"
STREAMLINK="${ROOT_DIR}/venv/bin/streamlink"
TARGET="target_url.txt"
INTERVAL=30
OUTPUT="${ROOT_DIR}/recordings/{author}/[{author}]{time:%Y-%m-%d-%H%M}_{title}_{id}.ts"
OPTIONS="--locale ko_KR --force --twitch-disable-hosting --twitch-disable-ads"
LOG_OPTIONS="--loglevel info --logfile ${ROOT_DIR}/logs/streamlink.log"
QUALITY="best"

stream() {
	$STREAMLINK --output "${OUTPUT}" $OPTIONS $LOG_OPTIONS $1 $QUALITY
	#wait
}

main() {
	echo ""
	echo "--streamlink--"
	echo "start recording!"
	echo "date : $(date +%y-%m-%d_%r)"
	for (( ; ; ))
	do
		i=0

		while read url; do
			streamer=${url:22}
			
			echo ""
			echo "check streaming.. > " $streamer
			echo "date : $(date +%y-%m-%d_%r)"
			
			stream_pid="`ps -ef | grep -v grep | grep $url | awk '{ print $2 }'`"
			if [ $stream_pid ]
			then
				echo "$streamer	is streaming! (pid:$stream_pid)"
				continue
			fi
			stream $url $i &
			((i++))
		done < $TARGET

		sleep $INTERVAL
	done
}

main
