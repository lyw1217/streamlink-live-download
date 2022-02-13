#!/bin/bash

CMD="streamlink"

echo "start streamlink"

pids=$(pgrep -f ${CMD})

if [ -n "$pids" ]; then
	echo "already running..."
	echo "[pids]"
	echo ${pids[@]}
	exit 0
fi

if [ ! -d "./logs" ] ; then
 mkdir ./logs
fi
/usr/bin/nohup /home/leeyw/Documents/github/streamlink-live-download/record.sh $CMD >> ./logs/nohup.log &

dot="...."
for i in 3 2 1
do
	echo "${dot:(-$i)}"
	sleep 1
done

pids=$(pgrep -f ${CMD})

echo "[pids]"
echo ${pids[@]}

echo "done!"
