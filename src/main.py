import subprocess as sp
import concurrent.futures as cf
import time
import datetime
import os

from getconfig import *

executor = cf.ThreadPoolExecutor(max_workers=32)

def create_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        root_logger.critical("Error : Creating directory " + directory)

# 채굴 시작
def start_mining(url):
    root_logger.critical(f"start mining... > '{url}'") 
    sp.Popen(['google-chrome-stable', url, '--new-window'])

# 채굴 종료
def stop_mining(author):
    root_logger.critical(f"stop mining... > '{author}'") 
    sp.call(['wmctrl', '-c', f'{author} - Twitch'])

# 스트리밍 중이라면 author metadata 반환, 아니면 '' 반환
def get_stream_info(streamer, url):
    root_logger.critical(f"get streaming information... > '{streamer}'") 

    title = ''
    author = ''

    args = list()
    opts = list()

    opts.append('--json')
    opts += f'{STREAMLINK_OPTIONS}'.split(' ')
    opts.append(f'{url}')

    args.append(STREAMLINK_CMD)
    args += opts
    pipe = sp.Popen(
        args, stdout=sp.PIPE
    )
    text = pipe.communicate()[0]

    dict = json.loads(text)
    for key, val in dict.items():
        if key == 'metadata':
            for k, v in val.items():
                if v != None:
                    if k == 'title':
                        title = v
                    elif k == 'author':
                        author = v
            break

    if len(title) > 0 and len(author) > 0:
        root_logger.critical(f"'{streamer}' is streaming!") 
        return author
    
    return ''

def upload_youtube(author, date) :
    print(f'upload_youtube author={author}, date={date}')

    file_list = os.listdir(OUTPUT_DIR)
    file_list_ts = [file for file in file_list if file.endswith(".ts")]

    for name in file_list_ts :
        if author in name :
            l_plus_date  = [date+datetime.timedelta(seconds=i) for i in range(15)]
            l_minus_date = [date-datetime.timedelta(seconds=i) for i in range(5)]

            # file name format : "[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts"
            file_date = datetime.datetime.strptime(name.split(']')[1][1:18], "%Y-%m-%d-%H%M%S")

            match_flag = False

            for d in l_plus_date :
                if file_date.hour == d.hour and file_date.minute == d.minute and file_date.second == d.second :
                    match_flag = True
                    break

            if match_flag == False :
                for d in l_minus_date :
                    if file_date.hour == d.hour and file_date.minute == d.minute and file_date.second == d.second :
                        match_flag = True
                        break
            
            if match_flag == True :
                root_logger.critical(f"youtube upload start {author} > file name : '{name}'")
                
                sp.call([PYTHON_CMD, UPLOAD_YOUTUBE_PY, 
                        '--file',           f'{OUTPUT_DIR}/{name}',
                        '--title',          f'{name}',
                        '--description',    f'{name}',
                        '--category',       "24",
                        '--privacyStatus',  "private"
                ])
                
                time.sleep(10)
                #root_logger.critical(f"remove {OUTPUT_DIR}/{name}")
                #os.remove(f"{OUTPUT_DIR}/{name}")
                break
    return

def start_streamlink(streamer, url):
    root_logger.critical(f"init check streaming thread... > '{streamer}'") 
    
    author = ''

    while True :
        author = get_stream_info(streamer, url)

        if author != '' :
            executor.submit(start_mining, url=url)
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

            date = datetime.datetime.now()

            sp.call(
                args
            )

            executor.submit(stop_mining, author=author)
            time.sleep(5)
            
            executor.submit(upload_youtube, author=author, date=date)
            author = ''
            time.sleep(5)

        time.sleep(INTERVAL)

    return

        
def check_stream():

    eof = True

    with open(TARGET_URL, "r") as f:
        while eof:
            url = f.readline().strip()
            if not url:
                eof = False
                continue

            # split url (https://www.twitch.tv/)
            name = url[22:].strip()
            executor.submit(start_streamlink, streamer=name, url=url)
            time.sleep(1)

    while True :
        time.sleep(100)
    
    return


if __name__ == '__main__':
    root_logger.critical("============================================")
    root_logger.critical("")
    root_logger.critical("       < PYSTREAMLINK >     S T A R T       ")
    root_logger.critical("         mining/upload      written by ywlee")
    root_logger.critical("============================================")
    create_dir(OUTPUT_DIR)
    check_stream()
