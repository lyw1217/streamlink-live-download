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
        root_logger.critical("Error : Creating directory " +  directory)

def start_streamlink(streamer, url) :
    root_logger.critical(f"START STREAMING > {streamer}")
    
    opt = f'--output "{OUTPUT_DIR}/{FILE_RULE}"' + ' '
    opt += f'{STREAMLINK_OPTIONS}' + ' '
    opt += f'{STREAMLINK_LOG_OPTIONS}' + ' '
    opt += f'--logfile {STREAMLINK_LOG_PATH}_{streamer}.log' + ' '
    opt += f'{url}' + ' '
    opt += f'{QUALITY}'

    result = sp.run(
        [STREAMLINK_CMD, opt]
        #, capture_output=True
        #, text=True
        , check=True
    )

    print(result)
    root_logger.critical(result)

    root_logger.critical(f"END STREAMING   > {streamer}")
    # 스트리밍 종료 시 딕셔너리에서 삭제
    del streamers[streamer]
    return

def check_stream() :
    executor = cf.ThreadPoolExecutor(max_workers=10)

    while True :
        eof = True
        with open(TARGET_URL, "r") as f :
            while eof :
                url = f.readline().strip()
                if not url:
                    eof = False
                    continue
                
                # split url (https://www.twitch.tv/)
                name = url[22:].strip()
                if name in streamers :
                    root_logger.critical(f"{name} is STREAMING!") 
                else :
                    streamers[name] = True
                    root_logger.critical(f"check streaming... > '{name}'")
                    executor.submit(start_streamlink, streamer=name, url=url)
                
                time.sleep(INTERVAL)
    return

if __name__ == '__main__' :
    root_logger.critical("============================================")
    root_logger.critical("")
    root_logger.critical("       < PYSTREAMLINK >     S T A R T       ")
    root_logger.critical("                            written by ywlee")
    root_logger.critical("============================================")
    create_dir(OUTPUT_DIR)
    check_stream()