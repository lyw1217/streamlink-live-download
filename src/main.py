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

    # print(args)

    sp.call(
        args
    )

    #parent_logger.info(f"END STREAMING   > {streamer}")
    # 스트리밍 종료 시 딕셔너리에서 삭제
    del streamers[streamer]
    return

def get_stream_info(streamer, url):
    title = ''
    author = ''
    date = time.strftime('%Y-%m-%d %H%M', time.localtime(time.time()))

    args = list()
    opts = list()

    opts.append('--json')
    opts += f'{STREAMLINK_OPTIONS}'.split(' ')
    opts.append(f'{url}')
    opts.append(f'{QUALITY}')

    args.append(STREAMLINK_CMD)
    args += opts
    pipe = sp.Popen(
        args
        , stdout = sp.PIPE
    )
    text = pipe.communicate()[0]

    dict = json.loads(text)
    for key, val in dict.items():
        if key == 'metadata' :
            for k, v in val.items():
                if k == 'title' :
                    title = v
                elif k == 'author' :
                    author = v

    if streamer in streamers :
        if len(title) > 0 and len(author) > 0 :
            streamers[streamer] = True 
            print(f'date = {date}')
            print(f'title = "{title}"')
            print(f'author = "{author}"')
            file_name = f"{OUTPUT_DIR}/[{author}]_{date}_{title}.ts.txt"
            print(file_name)
            with open(file_name, 'w') as f :
                f.write(file_name)
        
        

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

                print('streamers = ', streamers)
                # split url (https://www.twitch.tv/)
                name = url[22:].strip()
                if name in streamers:
                    parent_logger.info(f"{name} is streaming!!")
                    if streamers.get(name) == False :
                        get_stream_info(streamer=name, url=url)
                    time.sleep(INTERVAL)
                else:
                    streamers[name] = False
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
