FROM ubuntu:20.04
LABEL maintainer="mvl100d@gmail.com"
ENV IS_CONTAINER="True" \
    OUTPUT_DIR="/mnt/recordings" \ 
    SAVED_DIR="${OUTPUT_DIR}/saved"
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository universe
RUN apt install -y python3.8 python3-pip ffmpeg
RUN mkdir -p /app /mnt/recordings/saved
WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
ENTRYPOINT [ "python3", "./src/main.py" ]
