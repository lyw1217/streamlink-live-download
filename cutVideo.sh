#!/bin/bash

if [ $# -lt 1 ]; then
	echo "Usage : $0 {input_file.ts}"
	exit 0
fi

full_name=$1
echo "input file name = ${full_name}"

ext="${full_name:(-3)}"
name="${full_name:0:(-3)}"

if [ "$ext" != ".ts" ]; then
	echo "Only .ts file"
	exit 0
fi

echo "cut video, [start ~ 06:00:00 ] / [ 06:00:00 ~ end ]"

ffmpeg -i ${full_name} -t 06:00:00 -c:v copy -c:a copy ${name}_1.ts
ffmpeg -i ${full_name} -ss 06:00:00 -c:v copy -c:a copy ${name}_2.ts

echo "end.."
