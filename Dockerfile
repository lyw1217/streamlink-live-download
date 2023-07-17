FROM python:3.8-slim-buster
LABEL maintainer="mvl100d@gmail.com"
ARG RUNTIME_DIR=/app
ARG OUTPUT_DIR=/mnt/recordings
ARG SAVED_DIR=/mnt/recordings/saved

#RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN apt-get update \
	&& apt-get install -y apt-utils software-properties-common
RUN apt-get update \ 
	&& apt-get install -y --reinstall locales procps vim ffmpeg gcc libffi-dev \
	&& locale-gen ko_KR.UTF-8 \
	&& dpkg-reconfigure --frontend=noninteractive locales 
RUN localedef -f UTF-8 -i ko_KR ko_KR.UTF-8

RUN mkdir -p $RUNTIME_DIR/src \ 
			 $OUTPUT_DIR \ 
			 $SAVED_DIR

ENV IS_CONTAINER="True" \
    RUNTIME_DIR=${RUNTIME_DIR} \
    OUTPUT_DIR=${OUTPUT_DIR} \
    SAVED_DIR=${SAVED_DIR} \
    NAME=${NAME} \
	LANG="ko_KR.UTF-8" \
	LANGUAGE="ko_KR.UTF-8" \
	LC_ALL="ko_KR.UTF-8" \
	TZ=Asia/Seoul

WORKDIR $RUNTIME_DIR

COPY . .
COPY run.sh /run.sh
RUN chmod +x /run.sh

#RUN pip install --upgrade httplib2 uritemplate pyopenssl WebTest wheel apiclient \
#	pip install --upgrade oauth2client \
#	pip install --upgrade google-api-python-client \
#	pip install --upgrade streamlink

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /
RUN tar -cvf app.tar ./app
RUN mkdir -p /app/logs
WORKDIR $RUNTIME_DIR

ENTRYPOINT ../run.sh -c 2>&1 | tee -a /app/logs/run.log
