#!/bin/bash

ROOT_DIR="${HOME}/Documents/github/streamlink-live-download"
STREAMLINK="${ROOT_DIR}/venv/bin/streamlink"
TARGET="target_url.txt"
INTERVAL=20
OUTPUT="${ROOT_DIR}/recordings/{author}/[{author}]{time:%Y-%m-%d-%H%M}_{title}_{id}.ts"
OPTIONS="--locale ko_KR --force --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns"
LOG_OPTIONS="--loglevel trace --logfile ${ROOT_DIR}/logs/streamlink"
QUALITY="best"

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
			${STREAMLINK} --output "${OUTPUT}" ${OPTIONS} ${LOG_OPTIONS}_${streamer}.log ${url} ${QUALITY} &
			sleep 2
			((i++))
		done < $TARGET

		sleep $INTERVAL
	done
}

main
