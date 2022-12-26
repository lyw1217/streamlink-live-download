#-*- coding:utf-8 -*-
from concurrent.futures import thread
import subprocess as sp
import concurrent.futures as cf
import threading
from threading import Timer
import time
import datetime
import os
import smtplib
import requests
import schedule
from email.message import EmailMessage
from urllib import parse

from getconfig import *
from pipe import *
from slack import *

#executor = cf.ThreadPoolExecutor(max_workers=32)

upload_code = {}

def send_email(subject, content):
    '''
    # 이메일 주소 미설정 시 메일 전송기능 OFF
    if len(FROM_EMAIL_ADDR) == 0 or len(TO_EMAIL_ADDR) == 0 :
        return 
    root_logger.critical(f"Send Email, subject = {subject}, content = {content}")
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(content)

    # from == the sender's email address
    # to == the recipient's email address
    msg['Subject'] = f"[Pystreamlink] {subject}"
    msg['From'] = FROM_EMAIL_ADDR
    msg['To'] = TO_EMAIL_ADDR

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    root_logger.critical("Send Email Complete")
    '''

def init_slack_channel(channel_name: str):
    try:
        s = SlackAPI(SLACK_KEY)
        s.channel_id = s.get_channel_id(channel_name)
        root_logger.critical(f"Initialize Slack > channel_id = {s.channel_id}")
    except Exception as e:
        root_logger.critical(f"Failed init slack > channel_name = {channel_name}, err = {e}")

    return s

def post_slack_message(s: SlackAPI, text: str):
    if len(s.channel_id) > 0 :
        try :
            res = s.post_message(s.channel_id, text)
            root_logger.critical("Send Slack Message : " + text)
            return res
        except Exception as e:
            root_logger.critical(f"Failed Send Slack Message > id : {s.channel_id}, text : {text}, err = {e}")
            res = ""
            return res
    return ""
    

def get_slack_last_message(s: SlackAPI):
    if len(s.channel_id) > 0 :
        try :
            msg = s.get_last_message(s.channel_id)
            return msg
        except Exception as e:
            root_logger.critical(f"Failed Get Slack Message > id : {s.channel_id}, err = {e}")
            return None

def get_code_by_slack(p, s: SlackAPI, key: str):
    root_logger.critical("Init get code by slack thread...")
    global upload_code
    i = 0
    while True:
        i += 1
        if i > 239 : # 7200초 - 30초
            break
        try:
            message = get_slack_last_message(slack)
            
            if message != None and message["text"].startswith("auth") :
                if "latest_reply" in message :
                    upload_code[key] = s.get_thread_latest_message(s.channel_id, message['latest_reply'])
                    root_logger.critical(f"GET Youtube API Code = {upload_code[key]}")

                    root_logger.critical(f"code = {upload_code[key]}")
                    p_out = p.communicate(input=upload_code[key])[0]
                    post_slack_message(slack, f"Youtube API Token Refresh. out = {p_out}")
                    return

        except Exception as e:
            root_logger.critical(f"Failed get_code_by_slack err = {e}")
            return
        
        time.sleep(30)

    return


slack = init_slack_channel(SLACK_CHANNEL)

def create_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            root_logger.critical("Info : Creating directory " + directory)
    except (OSError, Exception):
        root_logger.critical("Error : Failed creating directory " + directory)
        sys.exit()

command = "which google-chrome-stable"
chk_chrome = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
CHROME_CMD = chk_chrome.communicate()[0].rstrip()
if "google-chrome-stable" not in CHROME_CMD :
    root_logger.critical("Info. google-chrome-stable not installed.. Don't Mine")

# 채굴 시작
def start_mining(url):
    if len(CHROME_CMD) != 0 or PIPE_FLAG == True :
        if PIPE_FLAG == True :
            root_logger.critical(f"start mining... > '{url}' using pipe")
            write_pipe(f"google-chrome-stable {url} --new-window")
        else :
            root_logger.critical(f"start mining... > '{url}'")
            try:
                p = sp.Popen(['google-chrome-stable', url, '--new-window'], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
                out = p.communicate()[0]
                root_logger.critical(out)
            except Exception as e:
                root_logger.critical(e)
                p.kill()
    
    return

# 채굴 종료
def stop_mining(author):
    if len(CHROME_CMD) != 0 or PIPE_FLAG == True :
        if PIPE_FLAG == True :
            root_logger.critical(f"stop mining... > '{author}' using pipe")
            write_pipe(f"wmctrl -c '{author} - Twitch'")
        else :
            root_logger.critical(f"stop mining... > '{author}'")
            #p = sp.Popen(['wmctrl', '-c', rf"'{author}' - Twitch"], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
            try:
                p = sp.Popen(['wmctrl', '-l'], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
                out = p.communicate()[0]
                tab = str()
                for t in out.split('\n'):
                    if author in t :
                        tab = ' '.join(t.split(' ')[4:])
                if tab is None :
                    root_logger.critical(f"tab is None..")
                else :    
                    root_logger.critical(f"tab = {tab}")
                    p = sp.Popen(['wmctrl', '-c', rf"{tab}"], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
            except Exception as e:
                root_logger.critical(e)
                p.kill()
    
    return

def get_stream_info_ytdlp(streamer, url):
    author = ''
    title = ''

    args = list()
    opts = list()

    opts.append('-j')
    opts.append(f'{url}')

    args.append(YTDLP_CMD)
    args += opts

    pipe = sp.Popen(
        args, stdout=sp.PIPE
    )
    try:
        text = pipe.communicate(timeout=60)[0]
    except Exception as e:
        pipe.kill()
        root_logger.critical(e)
        return "",""

    dict = json.loads(text)
    for key, val in dict.items():
        if key == 'description':
            title = val
        if key == 'uploader':
            author = val
        if len(title) > 0 and len(author) > 0:
            root_logger.critical(f"'{streamer}' is streaming!")
            root_logger.critical(f"METADATA : author = '{author}'")
            root_logger.critical(f"METADATA : title  = '{title}'")
            break

    return author, title

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
    try:
        # https://purplechip.tistory.com/1
        text = pipe.communicate(timeout=60)[0]
    except Exception as e:
        pipe.kill()
        root_logger.critical(e)
        return "",""

    dict = json.loads(text)
    
    for key, val in dict.items():
        if key == 'metadata':
            for k, v in val.items():
                if v != None:
                    if k == 'author':
                        author = v
                    elif k == 'title':
                        title = v
            # metadata가 항상 null인 방송은 yt-dlp 적용
            if len(author) == 0 and len(title) == 0:
                author, title = get_stream_info_ytdlp(streamer, url)
            break

    if len(author) > 0 and len(title) > 0:
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
    
        root_logger.critical(f"Err. upload_youtube.py Error occurred. err='{str}'")
    
    return False

def cmd_youtube_api(dir:str, name:str) :
    try:
        if len(IS_CONTAINER) > 0 :
            cmd = [PYTHON_CMD, '-u', UPLOAD_YOUTUBE_PY,
            '--file',            f'{dir}/{name}',
            '--title',          f'{name}',
            '--description',    f'{name}',
            '--category',       "24",
            '--privacyStatus',  "private",
            '--noauth_local_webserver'
            ]
        else :
            cmd = [PYTHON_CMD, UPLOAD_YOUTUBE_PY,
            '--file',            f'{dir}/{name}',
            '--title',          f'{name}',
            '--description',    f'{name}',
            '--category',       "24",
            '--privacyStatus',  "private"
            ]
        p = sp.Popen(
            cmd,
            stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True
        )

        timer = Timer(7200, p.kill)
        out = ""
        hash_key = hash(name) % 100000000
        global upload_code
        try :
            timer.start()
            while p.poll() == None:
                line = p.stdout.readline()
                out += line

                if "http" in line:
                    line = line.strip('\n').strip()
                    root_logger.critical(f"유튜브 토큰 만료. slack 채널에 'auth' 메시지를 전송하고 아래 링크로 발급받은 코드를 댓글로 남겨주세요.\n<{line}>")
                    post_slack_message(slack, f"유튜브 토큰 만료. slack 채널에 'auth' 메시지를 전송하고 아래 링크로 발급받은 코드를 댓글로 남겨주세요.")
                    post_slack_message(slack, f"<{line}>")
                    t = threading.Thread(target=get_code_by_slack,args=(p, slack,hash_key,))
                    t.start()
                else:
                    root_logger.critical(f"cmd_youtube_api({name}) STDOUT : '{out}'")
        finally:
            timer.cancel()
        # If your browser is on a different machine then exit and re-run this application with the command-line parameter '--noauth_local_webserver' 
        #outs = p.communicate(timeout=7200) # 2시간 동안 업로드하지 못했으면 timeout 처리

        return out

    except Exception as e:
        p.kill()
        outs = p.communicate()
        root_logger.critical(f"err = {repr(e)}")
        root_logger.critical(f"outs = {outs}")
        post_slack_message(slack, f"유튜브 업로드 중 실패. 토큰이 만료되었을 수 있습니다. > {e}\n\n{outs}")
        root_logger.critical(outs[0])

        return outs[0]
    
    return ""
    
    


def start_upload(author, name):
    root_logger.critical(f"youtube upload start {author} > file name : '{name}'")
    out = cmd_youtube_api(OUTPUT_DIR, name)

    if check_quota(out) :
        # 업로드 성공 시 파일 삭제
        root_logger.critical(f"Remove {OUTPUT_DIR}/{name}")
        #os.remove(f"{OUTPUT_DIR}/{name}")
        # 업로드 성공 시 파일 이동
        os.replace(f"{OUTPUT_DIR}/{name}", f"{UPLOADED_DIR}/{name}")
    else :
        root_logger.critical(f"Err. Failed upload youtube, Wait 60 seconds and Retry")
        # 1분 제한 회피
        time.sleep(60)
        # 업로드 실패 시 재시도
        root_logger.critical(f"RETRY youtube upload start {author} > file name : '{name}'")
        out = cmd_youtube_api(OUTPUT_DIR, name)

        if check_quota(out) :
            # 업로드 성공 시 파일 삭제
            root_logger.critical(f"RETRY Success upload youtube. Remove file")
            root_logger.critical(f"RETRY Remove {OUTPUT_DIR}/{name}")
            #os.remove(f"{OUTPUT_DIR}/{name}")
            # 업로드 성공 시 파일 이동
            os.replace(f"{OUTPUT_DIR}/{name}", f"{UPLOADED_DIR}/{name}")
        else :
            # 재시도 실패 시 임시 저장
            root_logger.critical(f"RETRY Err. Failed upload youtube. Replace file")
            root_logger.critical(f"RETRY Replace {OUTPUT_DIR}/{name} to {SAVED_DIR}/{name}")
            os.replace(f"{OUTPUT_DIR}/{name}", f"{SAVED_DIR}/{name}")
            send_email("유튜브 업로드 실패", f"파일명 : '{name}'\n 업로드 실패. 파일을 '{SAVED_DIR}/{name}' 경로로 이동하였습니다.")
            post_slack_message(slack, f"유튜브 업로드 실패, 파일명 : '{name}'\n 업로드 실패. 파일을 '{SAVED_DIR}/{name}' 경로로 이동하였습니다.")


def upload_youtube(author, title, date):
    root_logger.critical(f'upload_youtube author={author}, title={title}, date={date}')

    file_list = os.listdir(OUTPUT_DIR)
    file_list_ts = [file for file in file_list if file.endswith(".ts") or file.endswith(".mp4") or file.endswith(".m2ts")]
    
    match_flag = False

    for name in file_list_ts:
        if author in name:
            l_plus_date = [date+datetime.timedelta(seconds=i) for i in range(15)]
            l_minus_date = [date-datetime.timedelta(seconds=i) for i in range(5)]

            # file name format : "[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts"
            file_date = datetime.datetime.strptime(name.split(']')[1][1:18], "%Y-%m-%d-%H%M%S")

            root, ext = os.path.splitext(name)

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
                cut_count = cut_video(f"{OUTPUT_DIR}/{name}")
                root_logger.critical(f"Info. cut_video() END. cut_count = {cut_count}")
                if cut_count == 0 :
                    start_upload(author, name)
                elif cut_count > 0 :
                    # 30시간까지 가능
                    root_logger.critical(f"Info. upload cutted video. ")
                    if cut_count == 2 :
                        start_upload(author, f"{root}_1{ext}")      # 0 ~ 6
                        start_upload(author, f"{root}_2{ext}")      # 6 ~ 18
                    elif cut_count == 4 :
                        start_upload(author, f"{root}_1{ext}")      # 0 ~ 6
                        start_upload(author, f"{root}_2_1{ext}")    # 6 ~ 12
                        start_upload(author, f"{root}_2_2{ext}")    # 12 ~ 24
                    elif cut_count == 6 :
                        start_upload(author, f"{root}_1{ext}")      # 0 ~ 6
                        start_upload(author, f"{root}_2_1{ext}")    # 6 ~ 12
                        start_upload(author, f"{root}_2_2_1{ext}")  # 12 ~ 18
                        start_upload(author, f"{root}_2_2_2{ext}")  # 18 ~ 30
                    else :
                        send_email("유튜브 업로드 실패",
                        f"Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n 동영상을 자르는데 실패했습니다. 수동으로 자른 뒤 업로드해야 합니다.")
                        post_slack_message(slack, f"유튜브 업로드 실패, Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n 동영상을 자르는데 실패했습니다. 수동으로 자른 뒤 업로드해야 합니다.")
                else :
                    send_email("유튜브 업로드 실패",
                     f"Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n 동영상을 자르는데 실패했습니다. 수동으로 자른 뒤 업로드해야 합니다.")
                    post_slack_message(slack, f"유튜브 업로드 실패, Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n 동영상을 자르는데 실패했습니다. 수동으로 자른 뒤 업로드해야 합니다.")
                
                break

    if match_flag != True :
        root_logger.critical(f'Err. Failed upload_youtube author={author}, title={title}, date={date}, file_list_ts={file_list_ts}')
        send_email("유튜브 업로드 실패",
         f"Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n Streamlink에서 Metadata를 정상적으로 가져오지 못했습니다. 수동으로 업로드해야 합니다.")
        post_slack_message(slack, f"유튜브 업로드 실패, Title : {title}\nAuthor : {author}\nDate : {date}\n 파일 업로드 실패.\n Streamlink에서 Metadata를 정상적으로 가져오지 못했습니다. 수동으로 업로드해야 합니다.")

    return


def start_streamlink(streamer, url):
    root_logger.critical(f"Init check streaming thread... > '{streamer}'")
    post_slack_message(slack, f"스트리밍 확인 시작! > {streamer}")
    author = ''
    title = ''
    i = 0

    while True:
        try:
            if i % 100 == 0 :
                root_logger.critical(f"{datetime.datetime.now()} Get streaming information... > '{streamer}', i={i}")
            i += 1

            # youtube streaming의 경우 과부하 방지 목적으로 10번에 한 번 조회로 제한
            if "youtube" in url and i % 10 == 0:
                author, title = get_stream_info(streamer, url)
            elif "twitch" in url :
                author, title = get_stream_info(streamer, url)
            else :
                author = ''
                title = ''
    
            if author != '' and title != '':
                if MINING_FLAG == True :
                    #executor.submit(start_mining, url=url)
                    t1 = threading.Thread(target=start_mining, args=(url,))
                    t1.start()
                    time.sleep(1)
    
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
                try:
                    ps = sp.call(args)
                except Exception as e:
                    outs = ps.communicate()
                    root_logger.critical(f"Exception: {e}")
                    root_logger.critical(f"communicate : {outs[0]}")
    
                if MINING_FLAG == True :
                    #executor.submit(stop_mining, author=author)
                    t2 = threading.Thread(target=stop_mining, args=(author,))
                    t2.start()
                    #time.sleep(5)
    
                #executor.submit(upload_youtube, author=author, title=title, date=date)
                t3 = threading.Thread(target=upload_youtube, args=(author, title, date,))
                t3.start()
                i = 0
    
            author = ''
            title = ''
            time.sleep(INTERVAL)

        except Exception as e:
            root_logger.critical(f"Exception: {e}")

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
            name = url.split('/')[-1].strip()
            #executor.submit(start_streamlink, streamer=name, url=url)
            t = threading.Thread(target=start_streamlink, args=(name, url,))
            t.start()
            time.sleep(2)

    return

def upload_saved() :
    root_logger.critical(f"[SAVED] Start Upload youtube Saved Files ... ")
    file_list = os.listdir(SAVED_DIR)
    file_list_ts = [file for file in file_list if file.endswith(".ts") or file.endswith(".mp4") or file.endswith(".m2ts")]

    for name in file_list_ts:
        root_logger.critical(f"[SAVED] Try upload > {SAVED_DIR}/{name}")
        out = cmd_youtube_api(SAVED_DIR, name)

        if check_quota(out) :
            # 업로드 성공 시 파일 삭제
            root_logger.critical(f"[SAVED] Remove {SAVED_DIR}/{name}")
            #os.remove(f"{SAVED_DIR}/{name}")
            # 업로드 성공 시 파일 이동
            os.replace(f"{SAVED_DIR}/{name}", f"{UPLOADED_DIR}/{name}")
        else :
            root_logger.critical(f"[SAVED] Err. Failed upload youtube, Wait 60 seconds and Retry")
            # 1분 제한 회피
            time.sleep(60)
            # 업로드 실패 시 재시도
            out = cmd_youtube_api(SAVED_DIR, name)

            if check_quota(out) :
                # 업로드 성공 시 파일 삭제
                root_logger.critical(f"[SAVED] RETRY Success upload youtube. Remove file")
                root_logger.critical(f"[SAVED] RETRY Remove {OUTPUT_DIR}/{name}")
                #os.remove(f"{OUTPUT_DIR}/{name}")
                # 업로드 성공 시 파일 이동
                os.replace(f"{SAVED_DIR}/{name}", f"{UPLOADED_DIR}/{name}")
            else :
                # 재시도 실패 시 로깅
                root_logger.critical(f"[SAVED] RETRY Err. Failed upload youtube... CHECK QUOTA and FREE SPACE")
                send_email("SAVED 유튜브 업로드 실패", f"파일명 : '{name}'\n SAVED에 저장된 파일 업로드 실패.\n Google API의 할당량을 확인하세요.\n 다른 동영상 다운로드를 위해 하드디스크의 여유 공간을 확보하세요.")
                post_slack_message(slack, f"SAVED 유튜브 업로드 실패, 파일명 : '{name}'\n SAVED에 저장된 파일 업로드 실패.\n Google API의 할당량을 확인하세요.\n 다른 동영상 다운로드를 위해 하드디스크의 여유 공간을 확보하세요.")


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
    p = sp.Popen("df -h | grep -v '100%' | grep -v 'Use'| awk '{print $5}'", shell=True, text=True, stdout=sp.PIPE)

    result = p.stdout.read().split('\n')[:-1]
    uses = list()
    for r in result :
        r = r.strip()
        
        try :
            u = int(r[0 : len(r) - 1])
        except Exception as e:
            root_logger.critical(f"Err. Result is not Integer. result = '{r}', exception,  {str(e)}")
            u = 0

        uses.append(u)
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
            post_slack_message(slack, f"여유공간 확보 필요, 현재 다운로드된 동영상 용량 : {size} GB ({usage}% / 100%)\n다른 동영상 다운로드를 위해 하드디스크의 여유 공간을 확보하세요.")
        elif usage < WARN_USAGE :
            alarm_flag = False

        time.sleep(300)

# return : hour, minute, seconds
def get_duration(video_path):
    command = "which ffprobe"
    p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
    ffprobe_cmd = p.communicate()[0].rstrip()
    if "ffprobe" not in ffprobe_cmd :
        root_logger.critical("Err. ffmpeg not installed..")
        return (-1)
    
    command = [rf"{ffprobe_cmd} -i '{video_path}' 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//"]
    p = sp.Popen(command, stdout=sp.PIPE, text=True, shell=True)
    outs = p.communicate()
    
    duration = outs[0].rstrip().split(':')
    try :
        hour = int(duration[0])
        min = int(duration[1])
        sec = int(duration[2].split('.')[0])
    except (ValueError, IndexError, Exception) as e:
        root_logger.critical(f"Err. duration = {duration}, e='{str(e)}'")
        hour, min, sec = 0, 0, 0

    return hour

def cut_video(video_path) :
    h = get_duration(video_path)

    if h >= 12 :
        video_name, ext = os.path.splitext(video_path)
        cut_count = 0
        command = "which ffmpeg"
        p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
        ffmpeg_cmd = p.communicate()[0].rstrip()
        if "ffmpeg" not in ffmpeg_cmd :
            root_logger.critical("Err. ffmpeg not installed..")
            return (-1)
        
        command = [rf'{ffmpeg_cmd} -i "{video_path}" -to 06:00:02 -c:v copy -c:a copy "{video_name}_1{ext}"']
        root_logger.critical("cut video 00:00:00 ~ 06:00:02 start")
        try:
            p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
            outs = p.communicate(timeout=10800)
            root_logger.critical(outs[0])
            cut_count += 1
        except Exception as e :
            root_logger.critical("Err. cut_video()" + str(e))
            return (-1)
            
        
        root_logger.critical("cut video 05:59:58 ~ EOF start")
        command = [rf'{ffmpeg_cmd} -i "{video_path}" -ss 05:59:58 -c:v copy -c:a copy "{video_name}_2{ext}"']
        try:
            p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
            outs = p.communicate(timeout=10800)
            root_logger.critical(outs[0])
            cut_count += 1
        except Exception as e :
            root_logger.critical("Err. cut_video()" + str(e))
            return (-1)

        res = cut_video(f"{video_name}_2{ext}")
        if res < 0 :
            root_logger.critical("Err. Failed Cut Video")
            return (-1)
        
        root_logger.critical(f"Info. cut_count = {cut_count}, res = {res}")
        return cut_count + res

    return 0

# True : 토큰 갱신 필요(곧 expiry 됨), False : 토큰 갱신 미필요
def get_token_info(OAUTH_PATH):        
    with open(OAUTH_PATH, 'r', encoding='utf-8') as f :
        data = json.load(f)
        
        params = dict()
        params['client_id'] = data['client_id']
        params['client_secret'] = data['client_secret']
        params['access_token'] = data['access_token']

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        res = requests.post(data['token_info_uri'], params=params, headers=headers)
        
        json_res = res.json()
        if json_res.get('expires_in') :
            if int(json_res['expires_in']) < 120 :
                root_logger.critical("Token has expired!")
                return True
            else :
                return False
        else :
            return False

# https://developers.google.com/youtube/v3/live/guides/auth/devices#OAuth2_Refreshing_a_Token
def refresh_token():
    OAUTH_PATH = os.path.join(BASE_DIR, 'upload_youtube.py-oauth2.json')
    try :
        while True :
            if get_token_info(OAUTH_PATH) :
                root_logger.critical("Refresh Google Youtube API Access Token.")

                f = open(OAUTH_PATH, 'r', encoding='utf-8')
                data = json.load(f)
            
                params = dict()
                params['client_id'] = data['client_id']
                params['client_secret'] = data['client_secret']
                params['refresh_token'] = data['refresh_token']
                params['grant_type'] = 'refresh_token'

                headers = {'content-type': 'application/x-www-form-urlencoded'}
                res = requests.post(data['token_uri'], params=params, headers=headers)
                
                json_res = res.json()

                if json_res.get('access_token') :
                    data['access_token'] = json_res['access_token']
                    data['token_response']['access_token'] = json_res['access_token']
                    #print("data['access_token'] = ", data['access_token'])
                if json_res.get('refresh_token') :
                    data['refresh_token'] = json_res['refresh_token']
                    #print("data['refresh_token'] = ", data['refresh_token'])
                if json_res.get('expires_in') :
                    data['expires_in'] = json_res['expires_in']
                    data['token_response']['expires_in'] = json_res['expires_in']
                    #print("data['expires_in'] = ", data['expires_in'])

                new_expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(data['expires_in']))
                data['token_expiry'] = datetime.datetime.strftime(new_expiry, '%Y-%m-%dT%H:%M:%SZ')

                f.close()

                with open(OAUTH_PATH, 'w', encoding='utf-8') as f :
                    json.dump(data, f)
                    #print('Refresh Token End')

            time.sleep(60)
    except Exception as e :
        root_logger.critical("Err. Failed refresh_token() : " + str(e) )


if __name__ == '__main__':
    root_logger.critical("============================================")
    root_logger.critical("")
    root_logger.critical("       < PYSTREAMLINK >     S T A R T       ")
    if len(CHROME_CMD) != 0  and MINING_FLAG == True :
        root_logger.critical("         mining/upload      written by ywlee")
    elif len(CHROME_CMD) != 0 and PIPE_FLAG == True :
        root_logger.critical("          pipe/upload       written by ywlee")
    else :
        root_logger.critical("            upload          written by ywlee")
    root_logger.critical("============================================")
    
    create_dir(OUTPUT_DIR)
    create_dir(SAVED_DIR)
    create_dir(UPLOADED_DIR)
    #executor.submit(check_stream)
    t1 = threading.Thread(target=check_stream)
    t1.start()
    #executor.submit(check_filesystem)
    t2 = threading.Thread(target=check_filesystem)
    t2.start()
    #executor.submit(refresh_token)
    t3 = threading.Thread(target=refresh_token)
    t3.start()
    if PIPE_FLAG == True :
        create_pipe()

    schedule.every().day.at("14:00").do(upload_saved)
    schedule.every().day.at("17:05").do(upload_saved)
    upload_saved()
    root_logger.critical(f"[SAVED] Init upload saved ... ")
    while True :
        schedule.run_pending()
        time.sleep(1)
