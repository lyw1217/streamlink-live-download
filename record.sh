#!/bin/bash
HOME="/home/leeyw"
ROOT_DIR="${HOME}/Documents/github/streamlink-live-download"
STREAMLINK="${ROOT_DIR}/venv/bin/streamlink"
TARGET="${ROOT_DIR}/target_url.txt"
#OUTPUT_DIR="${ROOT_DIR}/recordings"
MOUNT_DIR="${HOME}/mnt"
OUTPUT_DIR="${MOUNT_DIR}/Twitch/recordings"
OUTPUT="${OUTPUT_DIR}/[{author}]_{time:%Y-%m-%d-%H%M}_{title}.ts"
OPTIONS="--locale en_US --force --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns"
LOG_FILE="${ROOT_DIR}/logs/streamlink"
LOG_OPTIONS="--loglevel info --logfile ${LOG_FILE}"
QUALITY="best"
INTERVAL=1

export LC_ALL="ko_KR.UTF-8" 
export LANG="ko_KR.UTF-8" 

chk_dir() {
	if [ ! -d "${OUTPUT_DIR}" ] ; then
		mkdir -p ${OUTPUT_DIR}
	fi
}

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

chk_dir

main
