#!/bin/bash

ROOT_DIR="${HOME}/Documents/github/streamlink-live-download"
STREAMLINK="${ROOT_DIR}/venv/bin/streamlink"
TARGET="${ROOT_DIR}/target_url.txt"
INTERVAL=5
OUTPUT="${ROOT_DIR}/recordings/{author}/[{author}]_{time:%Y-%m-%d-%H%M}_{title}.ts"
OPTIONS="--locale ko_KR --force --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns"
LOG_FILE="${ROOT_DIR}/logs/streamlink"
LOG_OPTIONS="--loglevel info --logfile ${LOG_FILE}"
QUALITY="best"

main() {
	echo ""
	echo "--streamlink--"
	echo "start recording!"
	echo "date : $(date +%y-%m-%d_%r)"
	for (( ; ; ))
	do
		i=0
		echo ""

		while read url; do
			streamer=${url:22}
			
			echo "check streaming.. > " $streamer
			echo "date : $(date +%y-%m-%d_%r)"
			
			stream_pid="`ps -ef | grep -v grep | grep $url | awk '{ print $2 }'`"
			if [ $stream_pid ]
			then
				echo "$streamer	is streaming! (pid:$stream_pid)"
				continue
			fi
			echo "date : $(date +%y-%m-%d_%r)" >> ${LOG_FILE}_${streamer}.log
			${STREAMLINK} --output "${OUTPUT}" ${OPTIONS} ${LOG_OPTIONS}_${streamer}.log ${url} ${QUALITY} &
			sleep 2
			((i++))
		done < $TARGET

		sleep $INTERVAL
	done
}

main
