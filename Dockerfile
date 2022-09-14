FROM python:3.8-slim
LABEL maintainer="mvl100d@gmail.com"
ARG RUNTIME_DIR=/app
ARG OUTPUT_DIR=/mnt/recordings
ARG SAVED_DIR=/mnt/recordings/saved

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN apt update \
	&& apt install -y software-properties-common
RUN apt update \ 
	&& apt install -y --reinstall locales && dpkg-reconfigure locales
RUN locale-gen ko_KR.UTF-8
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
	LC_ALL="ko_KR.utf8" \
	TZ=Asia/Seoul

WORKDIR $RUNTIME_DIR
COPY . .

RUN pip install -r ./requirements.txt

RUN pip install httplib2 uritemplate pyopenssl WebTest wheel apiclient \
	pip install --upgrade oauth2client \
	pip install --upgrade google-api-python-client \
	pip install --upgrade streamlink

ENTRYPOINT [ "python", "./src/main.py" ]
