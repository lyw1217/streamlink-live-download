#!/bin/bash

DOCKER=`which docker`

PYSTREAM_HOME="/home/leeyw/Documents/github/streamlink-live-download"

HOST_TARGET_URI="${PYSTREAM_HOME}/target_url.txt"
CONTAINER_TARGET_URI="/app/target_url.txt"

HOST_CONFIG="${PYSTREAM_HOME}/config/config.json"
CONTAINER_CONFIG="/app/config/config.json"

HOST_LOG_DIR="${PYSTREAM_HOME}/logs"
CONTAINER_LOG_DIR="/app/logs"

HOST_OUTPUT_DIR="/home/leeyw/mnt/Twitch/recordings"
CONTAINER_OUTPUT_DIR="/mnt/recordings"

HOST_SAVED_DIR="/home/leeyw/mnt/Twitch/recordings/saved"
CONTAINER_SAVED_DIR="/mnt/recordings/saved"

HOST_PIPE_PATH="${PYSTREAM_HOME}/fifo-pystream"
CONTAINER_PIPE_PATH="/app/fifo-pystream"

#HOST_CLIENT_SEC="${PYSTREAM_HOME}/src/client_secrets.json"
#CONTAINER_CLIENT_SEC="/app/src/client_secrets.json"

#HOST_OAUTH="${PYSTREAM_HOME}/src/upload_youtube.py-oauth2.json"
#CONTAINER_OAUTH="/app/src/upload_youtube.py-oauth2.json"

CLIENT_ID=$CLIENT_ID=""
CLIENT_SECRET=$CLIENT_SECRET=""
PROJECT_ID=$PROJECT_ID=""
ACCESS_TOKEN=$ACCESS_TOKEN=""
REFRESH_TOKEN=$REFRESH_TOKEN=""
FROM_EMAIL_ADDR=""
TO_EMAIL_ADDR=""
SLACK_CHANNEL=""
SLACK_KEY=""

if [ $# -lt 4 ] ; then
	echo
    echo "Usage : $0 [container name] [image name] [tag] [it | d]"
	echo
	echo "--Docker Images--"
	$DOCKER images
    exit 0
fi

CONTAINER_NAME=$1
IMAGE_NAME=$2
IMAGE_TAG=$3

#echo
#PID=$(pgrep -f "readPipe")
#echo $PID
#if [ -n "$PID" ]; then
#	echo "kill -9 pid : $PID"
#	KILL=`which kill`
#	$KILL -9 $PID
#fi
#echo "run readPipe.sh"
#/bin/bash ./readPipe.sh &

if [ "$4" == "it" ]; then
	echo "container run in interactive (--interactive --tty)"
	
else
	echo "container run in only background (--detach)"
fi

if [ -n "$($DOCKER ps -aq --filter "name=${CONTAINER_NAME}")" ]; then
	$DOCKER stop ${CONTAINER_NAME} && $DOCKER rm -f ${CONTAINER_NAME}
fi

echo

$DOCKER run -$4 --name $CONTAINER_NAME \
-v $HOST_TARGET_URI:$CONTAINER_TARGET_URI \
-v $HOST_CONFIG:$CONTAINER_CONFIG \
-v $HOST_OUTPUT_DIR:$CONTAINER_OUTPUT_DIR \
-v $HOST_SAVED_DIR:$CONTAINER_SAVED_DIR \
-v $HOST_PIPE_PATH:$CONTAINER_PIPE_PATH \
-v $HOST_LOG_DIR:$CONTAINER_LOG_DIR \
-e CLIENT_ID=$CLIENT_ID \
-e CLIENT_SECRET=$CLIENT_SECRET \
-e PROJECT_ID=$PROJECT_ID \
-e ACCESS_TOKEN=$ACCESS_TOKEN \
-e REFRESH_TOKEN=$REFRESH_TOKEN \
$IMAGE_NAME:$IMAGE_TAG bash
