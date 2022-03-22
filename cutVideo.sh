#!/bin/bash


#if [ $# -lt 1 ]; then
#	echo ""
#	echo "Usage : $0 {input_file.ts}"
#	echo ""
#	exit 0
#fi

VIDEO_PATH="/home/leeyw/mnt/Twitch/recordings"

for arg in "$VIDEO_PATH"/*
do
	if [ ! -e "$arg" ]; then
		echo "File "$arg" is not exists."
		continue
	fi

	full_name=$arg
	ext="${full_name:(-3)}"
	name="${full_name:0:(-3)}"

	if [ "$ext" != ".ts" ]; then
		#echo ""
		#echo "Only .ts file"
		#echo ""
		continue
	fi
	
	echo ""
	echo "Input file name = ${full_name}"

	duration=$(ffmpeg -i $arg 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//)
	echo "Duration : ${duration}"

	if [ "${duration:0:2}" -lt "12" ]; then
		echo ""
		echo "This Video is shorter than 12 hours. Just Upload it."
		echo ""
		continue
	fi

	echo ""
	echo "cut video, [00:00:00 ~ 06:00:00 ] / [ 06:00:00 ~ ${duration} ]"

	#ffmpeg -i ${full_name} -ss 00:00:00 -to 06:00:02 -c:v copy -c:a copy ${name}_1.ts
	ffmpeg -i ${full_name} -to 06:00:02 -c:v copy -c:a copy ${name}_1.ts
	sleep 5
	#ffmpeg -i ${full_name} -ss 05:59:58 -to ${duration} -c:v copy -c:a copy ${name}_2.ts
	ffmpeg -i ${full_name} -ss 05:59:58 -c:v copy -c:a copy ${name}_2.ts

done

echo "end.."
