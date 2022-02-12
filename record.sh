#!/bin/bash

STREAMLINK="./venv/bin/streamlink"
TARGET="target_url.txt"
INTERVAL=30
OUTPUT="./recordings/{author}/[{author}]{time:%Y-%m-%d}_{title}.ts"
OPTIONS="--force --twitch-disable-hosting --twitch-disable-ads"
QUALITY="best"

stream() {
	$STREAMLINK --output "${OUTPUT}" $OPTIONS $1 $QUALITY
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
