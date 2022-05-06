import subprocess as sp
import concurrent.futures as cf
import time
import datetime
import os
import smtplib
from email.message import EmailMessage

from getconfig import *

executor = cf.ThreadPoolExecutor(max_workers=32)

def send_email(subject, content):
    # 이메일 주소 미설정 시 메일 전송기능 OFF
    if len(FROM_EMAIL_ADDR) == 0 or len(TO_EMAIL_ADDR) == 0 :
        return 
    root_logger.critical(f"Send Email, subject = {subject}, content = {content}")
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(content)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f"[Pystreamlink] {subject}"
    msg['From'] = FROM_EMAIL_ADDR
    msg['To'] = TO_EMAIL_ADDR

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    root_logger.critical("Send Email Complete")


def create_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        root_logger.critical("Error : Creating directory " + directory)


# 채굴 시작
def start_mining(url):
    root_logger.critical(f"start mining... > '{url}'")
    p = sp.Popen(['google-chrome-stable', url, '--new-window'], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
    out = p.communicate()[0]
    root_logger.critical(out)

# 채굴 종료
def stop_mining(author):
    root_logger.critical(f"stop mining... > '{author}'")
    p = sp.run(['wmctrl', '-c', f'{author} - Twitch'], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
    out = p.communicate()[0]
    root_logger.critical(out)


# 스트리밍 중이라면 author metadata 반환, 아니면 '' 반환
def get_stream_info(streamer, url):
    author = ''
    title = ''

    args = list()
    opts = list()

    opts.append('--json')
    opts += f'{STREAMLINK_OPTIONS}'.split(' ')  # --twitch-disable-hosting 옵션이 없으면 호스팅 시 metadata mismatch 발생
    opts.append(f'{url}')

    args.append(STREAMLINK_CMD)
    args += opts
    pipe = sp.Popen(
        args, stdout=sp.PIPE
    )
    # https://purplechip.tistory.com/1
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
        root_logger.critical(f"METADATA : author = '{author}'")
        root_logger.critical(f"METADATA : title  = '{title}'")

    return author, title

'''
성공 시 stdout 메시지
"Uploading file...\nVideo id 'abcdefg12345' was successfully uploaded.\n"

실패 시 stdout 메시지
'Uploading file...\nAn HTTP error 403 occurred:\nb\'{\\n  "error": {\\n    "code": 403,\\n    "message": "The request cannot be completed because you have exceeded your \\\\u003ca href=\\\\"/youtube/v3/getting-started#quota\\\\"\\\\u003equota\\\\u003c/a\\\\u003e.",\\n    "errors": [\\n      {\\n        "message": "The request cannot be completed because you have exceeded your \\\\u003ca href=\\\\"/youtube/v3/getting-started#quota\\\\"\\\\u003equota\\\\u003c/a\\\\u003e.",\\n        "domain": "youtube.quota",\\n        "reason": "quotaExceeded"\\n      }\\n    ]\\n  }\\n}\\n\'\n'
'''
def check_quota(str):
    if 'successfully' in str :
        return True
    else : 
        if 'error 403' in str or '"code": 403' in str :
            if 'quotaExceeded' in str :
                root_logger.critical("Err. quotaExceeded.")
                return False
    
        root_logger.critical("Err. Unknown Error occurred.")
    
    return False

def cmd_youtube_api(dir, name) :
    p = sp.Popen([PYTHON_CMD, UPLOAD_YOUTUBE_PY,
            '--file',            f'{dir}/{name}',
            '--title',          f'{name}',
            '--description',    f'{name}',
            '--category',       "24",
            '--privacyStatus',  "private"
            ], 
            stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
    try:
        outs = p.communicate(timeout=7200) # 2시간 동안 업로드하지 못했으면 timeout 처리
    except:
        p.kill()
        outs = p.communicate()
    
    root_logger.critical(outs[0])
    return outs[0]


def upload_youtube(author, title, date):
    root_logger.critical(f'upload_youtube author={author}, title={title}, date={date}')

    file_list = os.listdir(OUTPUT_DIR)
    file_list_ts = [file for file in file_list if file.endswith(".ts")]
    
    match_flag = False

    for name in file_list_ts:
        if author in name:
            l_plus_date = [
                date+datetime.timedelta(seconds=i) for i in range(15)]
            l_minus_date = [
                date-datetime.timedelta(seconds=i) for i in range(5)]

            # file name format : "[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts"
            file_date = datetime.datetime.strptime(name.split(']')[1][1:18], "%Y-%m-%d-%H%M%S")

            match_flag = False

            for d in l_plus_date:
                if file_date.hour == d.hour and file_date.minute == d.minute and file_date.second == d.second:
                    match_flag = True
                    break

            if match_flag == False:
                for d in l_minus_date:
                    if file_date.hour == d.hour and file_date.minute == d.minute and file_date.second == d.second:
                        match_flag = True
                        break

            if match_flag == True:
                root_logger.critical(f"youtube upload start {author} > file name : '{name}'")
                out = cmd_youtube_api(OUTPUT_DIR, name)

                if check_quota(out) :
                    # 업로드 성공 시 파일 삭제
                    root_logger.critical(f"Remove {OUTPUT_DIR}/{name}")
                    #os.remove(f"{OUTPUT_DIR}/{name}")
                else :
                    root_logger.critical(f"Err. Failed upload youtube, Wait 60 seconds and Retry")
                    # 1분 제한 회피
                    time.sleep(60)
                    # 업로드 실패 시 재시도
                    root_logger.critical(f"RETRY youtube upload start {author} > file name : '{name}'")
                    out = cmd_youtube_api(OUTPUT_DIR, name)

                    if check_quota(out) :
                        root_logger.critical(f"RETRY Success upload youtube. Remove file")
                        root_logger.critical(f"RETRY Remove {OUTPUT_DIR}/{name}")
                        #os.remove(f"{OUTPUT_DIR}/{name}")
                    else :
                        # 재시도 실패 시 임시 저장
                        root_logger.critical(f"RETRY Err. Failed upload youtube. Replace file")
                        root_logger.critical(f"RETRY Replace {OUTPUT_DIR}/{name} to {SAVED_DIR}/{name}")
                        os.replace(f"{OUTPUT_DIR}/{name}", f"{SAVED_DIR}/{name}")
                        send_email("유튜브 업로드 실패", f"파일명 : '{name}'\n 업로드 실패. 파일을 '{SAVED_DIR}/{name}' 경로로 이동하였습니다.")
                break

    if match_flag != True :
        root_logger.critical(f'Err. Failed upload_youtube author={author}, title={title}, date={date}, file_list_ts={file_list_ts}')
        send_email("유튜브 업로드 실패", f"Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n Streamlink에서 Metadata를 정상적으로 가져오지 못했습니다. 수동으로 업로드해야합니다.")

    return


def start_streamlink(streamer, url):
    root_logger.critical(f"Init check streaming thread... > '{streamer}'")

    author = ''
    title = ''
    i = 0

    while True:
        if i % 100 == 0 :
            root_logger.critical(f"{datetime.datetime.now()} Get streaming information... > '{streamer}'")
            i = 0
        i += 1

        author, title = get_stream_info(streamer, url)

        if author != '' and title != '':
            time.sleep(1)
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

            sp.call(args)
            
            time.sleep(1)
            executor.submit(stop_mining, author=author)
            time.sleep(5)

            executor.submit(upload_youtube, author=author, title=title, date=date)
            time.sleep(10)
            i = 0

        author = ''
        title = ''
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
            time.sleep(2)

    return

def upload_saved() :
    root_logger.critical(f"[SAVED] Init upload saved ... ")
    f_once = False
    while True:
        date = datetime.datetime.now()

        if date.hour == 17 and date.minute >= 10 and date.minute <= 11 and f_once == False :
            root_logger.critical(f"[SAVED] Start Upload youtube Saved Files ... ")
            file_list = os.listdir(SAVED_DIR)
            file_list_ts = [file for file in file_list if file.endswith(".ts")]

            for name in file_list_ts:
                out = cmd_youtube_api(SAVED_DIR, name)

                if check_quota(out) :
                    # 업로드 성공 시 파일 삭제
                    root_logger.critical(f"[SAVED] Remove {SAVED_DIR}/{name}")
                    #os.remove(f"{SAVED_DIR}/{name}")
                else :
                    root_logger.critical(f"[SAVED] Err. Failed upload youtube, Wait 60 seconds and Retry")
                    # 1분 제한 회피
                    time.sleep(60)
                    # 업로드 실패 시 재시도
                    out = cmd_youtube_api(SAVED_DIR, name)

                    if check_quota(out) :
                        root_logger.critical(f"[SAVED] RETRY Success upload youtube. Remove file")
                        root_logger.critical(f"[SAVED] RETRY Remove {OUTPUT_DIR}/{name}")
                        #os.remove(f"{OUTPUT_DIR}/{name}")
                    else :
                        # 재시도 실패 시 로깅
                        root_logger.critical(f"[SAVED] RETRY Err. Failed upload youtube... CHECK QUOTA and FREE SPACE")
                        send_email("SAVED 유튜브 업로드 실패", f"파일명 : '{name}'\n SAVED에 저장된 파일 업로드 실패.\n Google API의 할당량을 확인하세요.\n 다른 동영상 다운로드를 위해 하드디스크의 여유 공간을 확보하세요.")
                break

            f_once = True
            time.sleep(60)
        
        if date.hour >= 18:
            f_once = False

        time.sleep(10)

# https://codechacha.com/ko/python-file-or-dir-size/
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    # return unit : gigabytes
    return total // (1024 * 1024 * 1024)

def get_filesystem_use():
    pipe = sp.Popen("df -h | grep -v '100%' | grep -v 'Use'| awk '{print $5}'", shell=True, text=True, stdout=sp.PIPE)

    result = pipe.stdout.read().split('\n')[:-1]
    uses = list()
    for r in result :
        r = r.strip()
        uses.append(int(r[0 : len(r) - 1]))
    return max(uses)

def check_filesystem() :
    root_logger.critical("Init check filesystem thread...")
    alarm_flag = False

    while True :
        usage = get_filesystem_use()
        
        if usage >= WARN_USAGE and alarm_flag == False:
            alarm_flag = True
            size = get_dir_size(OUTPUT_DIR)
            root_logger.critical("Warning! Low Disk Space. Delete Videos")
            send_email("여유공간 확보 필요", f"현재 다운로드된 동영상 용량 : {size} GB ({usage}% / 100%)\n다른 동영상 다운로드를 위해 하드디스크의 여유 공간을 확보하세요.")
        elif usage < WARN_USAGE :
            alarm_flag = False

        time.sleep(300)


if __name__ == '__main__':
    root_logger.critical("============================================")
    root_logger.critical("")
    root_logger.critical("       < PYSTREAMLINK >     S T A R T       ")
    root_logger.critical("         mining/upload      written by ywlee")
    root_logger.critical("============================================")
    
    create_dir(OUTPUT_DIR)
    create_dir(SAVED_DIR)
    executor.submit(check_stream)
    executor.submit(check_filesystem)
    upload_saved()
    

