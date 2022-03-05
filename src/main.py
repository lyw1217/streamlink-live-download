import subprocess as sp
import concurrent.futures as cf
import time
import os

from getconfig import *

streamers = dict()


def create_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        root_logger.critical("Error : Creating directory " + directory)


def start_streamlink(streamer, url):
    #parent_logger.info(f"START STREAMING > {streamer}")

    args = list()
    opts = list()

    opts.append('--output')
    opts.append(f'{OUTPUT_DIR}/{FILE_RULE}')
    opts += f'{STREAMLINK_OPTIONS}'.split(' ')
    opts.append('--loglevel')
    opts.append(f'{STREAMLINK_LOG_OPTIONS}')
    opts.append('--logfile')
    opts.append(f'{STREAMLINK_LOG_PATH}_{streamer}.log')
    opts.append(f'{url}')
    opts.append(f'{QUALITY}')

    args.append(STREAMLINK_CMD)
    args += opts

    print(args)

    sp.call(
        args
        # capture_output=True, text=True,
        # check=True
    )

    #parent_logger.info(f"END STREAMING   > {streamer}")
    # 스트리밍 종료 시 딕셔너리에서 삭제
    del streamers[streamer]
    return


def check_stream():
    executor = cf.ThreadPoolExecutor(max_workers=10)

    while True:
        eof = True
        with open(TARGET_URL, "r") as f:
            while eof:
                url = f.readline().strip()
                if not url:
                    eof = False
                    continue

                # split url (https://www.twitch.tv/)
                name = url[22:].strip()
                if name in streamers:
                    #parent_logger.info(f"{name} is streaming!!")
                    time.sleep(INTERVAL)
                else:
                    streamers[name] = True
                    root_logger.critical(f"check streaming... > '{name}'")
                    executor.submit(start_streamlink, streamer=name, url=url)
                    time.sleep(INTERVAL)

    return


if __name__ == '__main__':
    root_logger.critical("============================================")
    root_logger.critical("")
    root_logger.critical("       < PYSTREAMLINK >     S T A R T       ")
    root_logger.critical("                            written by ywlee")
    root_logger.critical("============================================")
    create_dir(OUTPUT_DIR)
    check_stream()
