#!/bin/bash

PIPE_PATH="${HOME}/Documents/github/streamlink-live-download/fifo-pystream"
LOG_PATH="${HOME}/Documents/github/streamlink-live-download/logs"

if [ ! -e $PIPE_PATH ]; then
    echo "Pipe does not exist."
    exit
fi

while true
do
    pipe_cmd="$(cat ${PIPE_PATH})"
    echo "[`date`] > $pipe_cmd" >> ${LOG_PATH}/pipe.log 2>&1
    eval "$pipe_cmd" & >> ${LOG_PATH}/pipe.log 2>&1
done