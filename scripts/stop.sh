#!/bin/bash

CMD="streamlink"

echo "stop streamlink"

pids=$(pgrep -f ${CMD})
if [ -z "${pids}" ]; then
	echo "There is no running process. exit.."
	exit 0
fi
echo "kill -15"
echo "[pids]"
echo ${pids[@]}
kill -15 $pids

dot="...."
for i in 3 2 1
do
	echo "${dot:(-$i)}"
	sleep 1
done

pids=$(pgrep -f ${CMD})
if [ $pids ]; then
	echo "remaining pids"
	echo "$pids[@]"
	echo ""
	echo "kill -9"
	echo "[pids]"
	echo ${pids[@]}
	kill -9 $pids
fi

echo "done!"
