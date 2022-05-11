ARG RUNTIME_DIR=/app
ARG OUTPUT_DIR=/mnt/recordings
ARG SAVED_DIR=/mnt/recordings/saved
ARG NAME=pystream

FROM python:3.8 AS builder
LABEL stage=builder
ARG RUNTIME_DIR
ARG OUTPUT_DIR
ARG SAVED_DIR
ARG NAME
ENV IS_CONTAINER="True" \
    RUNTIME_DIR=${RUNTIME_DIR} \
    OUTPUT_DIR=${OUTPUT_DIR} \
    SAVED_DIR=${SAVED_DIR} \
    NAME=${NAME}
RUN mkdir -p $RUNTIME_DIR
WORKDIR $RUNTIME_DIR
COPY . .
RUN pip install -r ./requirements.txt
RUN pip install --upgrade pyinstaller
RUN pyinstaller --onefile --clean --name $NAME --runtime-tmpdir $RUNTIME_DIR src/main.py

FROM ubuntu:20.04
LABEL maintainer="mvl100d@gmail.com"
ARG RUNTIME_DIR
ARG OUTPUT_DIR
ARG SAVED_DIR
ARG NAME
ENV IS_CONTAINER="True" \
    RUNTIME_DIR=${RUNTIME_DIR} \
    OUTPUT_DIR=${OUTPUT_DIR} \
    SAVED_DIR=${SAVED_DIR} \
    NAME=${NAME}
RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN apt-get update \
	&& apt-get install -y software-properties-common \
    && add-apt-repository universe
RUN apt-get update && apt-get install -y python3.8 python3-pip ffmpeg
RUN pip install --upgrade streamlink
RUN mkdir -p $RUNTIME_DIR/src $OUTPUT_DIR $SAVED_DIR
WORKDIR $RUNTIME_DIR
COPY --chown=0:0 --from=builder $RUNTIME_DIR/dist/${NAME} .
COPY --chown=0:0 --from=builder $RUNTIME_DIR/src ./src/upload_youtube.py
COPY --chown=0:0 --from=builder $RUNTIME_DIR/config ./config
COPY --chown=0:0 --from=builder $RUNTIME_DIR/target_url.txt ./target_url.txt
ENTRYPOINT [ "/bin/bash", "-c", "./${NAME}" ]
