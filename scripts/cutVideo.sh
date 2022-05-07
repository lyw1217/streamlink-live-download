#!/bin/bash

# 길이가 12시간을 넘는 영상을 6시간 기준으로 자르는 스크립트

#if [ $# -lt 1 ]; then
#	echo ""
#	echo "Usage : $0 {input_file.ts}"
#	echo ""
#	exit 0
#fi

VIDEO_PATH="${HOME}/mnt/Twitch/recordings"

IS_OVER=0

PROGRAM="ffmpeg"
CMD=`command -v ${PROGRAM} 2>/dev/null`

if [ ! -d ${VIDEO_PATH} ]; then
    echo "'${VIDEO_PATH}' Directory does not exist!"
    echo "exit"
    exit
fi

if [ -z "$CMD" ]; then
    echo "${PROGRAM} command does not exist!"
    echo "Please, Install ffmpeg. refer to https://ffmpeg.org/download.html"
    echo "exit"
    exit
fi 

cut_video() {
	for arg in "$1"/*
	do
		if [ ! -e "$arg" ]; then
			echo "File "$arg" is not exists."
			continue
		fi

		full_name=$arg
		ext="${full_name:(-3)}"
		name="${full_name:0:(-3)}"

		if [ "$ext" != ".ts" ]; then
			continue
		fi

		duration=$(${CMD} -i "${arg}" 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//)
		if [ "${duration:0:2}" -lt "12" ]; then
			continue
		fi

		echo ""
		echo "Input file name = ${full_name}"
		echo "Duration : ${duration}"

		echo ""
		echo "cut video, [00:00:00 ~ 06:00:00 ] / [ 06:00:00 ~ ${duration} ]"

		#ffmpeg -i ${full_name} -ss 00:00:00 -to 06:00:02 -c:v copy -c:a copy ${name}_1.ts
		$CMD -i "${full_name}" -to 06:00:02 -c:v copy -c:a copy "${name}_1.ts"
		sleep 5
		#ffmpeg -i ${full_name} -ss 05:59:58 -to ${duration} -c:v copy -c:a copy ${name}_2.ts
		$CMD -i "${full_name}" -ss 05:59:58 -c:v copy -c:a copy "${name}_2.ts"

	done
}

check_duration() {
	for arg in "$1"/*
	do
		echo "check duration ${arg}..."
		if [ ! -e "$arg" ]; then
			echo "No Files found in '$arg'"
			continue
		fi

		if [ -d "$arg" ]; then
			check_duration $arg
			continue
		fi

		full_name=$arg
		ext="${full_name:(-3)}"
		name="${full_name:0:(-3)}"

		if [ "$ext" != ".ts" ]; then
			continue
		fi
		
		echo ""
		echo "Input file name = ${full_name}"

		duration=$(${CMD} -i "${arg}" 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//)
		echo "Duration : ${duration}"

		if [ "${duration:0:2}" -lt "12" ]; then
			echo "This Video is shorter than 12 hours. Just Upload it."
			echo ""
			continue
		fi

		IS_OVER=1
		break
	done

	if [ $IS_OVER -eq 1 ]; then 
		read -p "There are more than 12 hours of video. Do you want to cut it? (y,n) " usr_input
		# cut video
		if [ ${usr_input} == 'y' ] || [ ${usr_input} == 'Y' ]; then
			cut_video $VIDEO_PATH
		fi
	fi
}

check_duration $VIDEO_PATH

echo "end.."

sleep 1
