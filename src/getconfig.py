#-*- coding:utf-8 -*-
import os
import sys
import json
import platform
import logging
import logging.config
import subprocess as sp

def create_log_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Info : Creating directory " + directory)
    except (OSError, Exception):
        print("Error : Failed creating directory " + directory)
        sys.exit()

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
SYS_PLATFORM = platform.system()

create_log_dir(os.path.join(ROOT_DIR, 'logs'))

''' Logging Configuration '''
if SYS_PLATFORM == 'Windows':
    LOGGING_PATH = os.path.join(ROOT_DIR, r'config\logging.json')
else :
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config/logging.json')

if os.path.isfile(LOGGING_PATH):
    with open(LOGGING_PATH) as json_file:
        log_configs = json.load(json_file)
        try :
            log_filename = log_configs ['handlers']['file']['filename']
            if SYS_PLATFORM == 'Windows':
                log_configs ['handlers']['file']['filename'] = os.path.join(ROOT_DIR, fr'logs\{log_filename}')
            else :
                log_configs ['handlers']['file']['filename'] = os.path.join(ROOT_DIR, f'logs/{log_filename}')
        except Exception :
            print("failed to load logging.json")
            sys.exit()
        logging.config.dictConfig(log_configs)
    root_logger = logging.getLogger()
    '''
    # USAGE
    root_logger.debug("디버그")
    root_logger.info("정보")
    root_logger.error("오류")
    '''
    parent_logger = logging.getLogger("parent")
    '''
    # USAGE
    parent_logger.debug("디버그")
    parent_logger.info("정보")
    parent_logger.error("오류")
    '''
    child_logger = logging.getLogger("parent.child")
    '''
    # USAGE
    child_logger.debug("디버그")
    child_logger.info("정보")
    child_logger.error("오류")
    '''
else :
    print("logging.json file is not exist")
    sys.exit()



''' Main Configuration '''
if SYS_PLATFORM == 'Windows':
    CONFIG_PATH = os.path.join(ROOT_DIR, r'config\config.json')
else :
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')

IS_CONTAINER = os.getenv("IS_CONTAINER", "")
# container 인 경우
if len(IS_CONTAINER) > 0 :
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH) as json_file :
            configs = json.load(json_file)

            root_logger.critical('=== CONTAINER CONFIGURATIONS LOADED ===')
            INTERVAL = configs['INTERVAL']
            root_logger.critical(f'INTERVAL = {INTERVAL}')
            QUALITY = configs['QUALITY']
            root_logger.critical(f'QUALITY = {QUALITY}')
            OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/mnt/recordings")
            root_logger.critical(f'OUTPUT_DIR = {OUTPUT_DIR}')
            FILE_RULE = "[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts"
            root_logger.critical(f'FILE_RULE = {FILE_RULE}')
            TARGET_URL = os.path.join(ROOT_DIR, "target_url.txt")
            root_logger.critical(f'TARGET_URL = {TARGET_URL}')
            command = "which streamlink"
            p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
            STREAMLINK_CMD = p.communicate()[0].rstrip()
            if "streamlink" not in STREAMLINK_CMD :
                root_logger.critical("Err. streamlink not installed..")
                sys.exit()
            root_logger.critical(f'STREAMLINK_CMD = {STREAMLINK_CMD}')
            STREAMLINK_OPTIONS = configs['STREAMLINK_OPTIONS']
            root_logger.critical(f'STREAMLINK_OPTIONS = {STREAMLINK_OPTIONS}')
            STREAMLINK_LOG_OPTIONS = configs['STREAMLINK_LOG_OPTIONS']
            root_logger.critical(f'STREAMLINK_LOG_OPTIONS = {STREAMLINK_LOG_OPTIONS}')
            STREAMLINK_LOG_PATH = os.path.join(ROOT_DIR, "logs/streamlink")
            root_logger.critical(f'STREAMLINK_LOG_PATH = {STREAMLINK_LOG_PATH}')
            UPLOAD_YOUTUBE_PY = os.path.join(ROOT_DIR, "src/upload_youtube.py")
            root_logger.critical(f'UPLOAD_YOUTUBE = {UPLOAD_YOUTUBE_PY}')
            if not os.path.isfile(UPLOAD_YOUTUBE_PY):
                root_logger.critical(f'Err. {UPLOAD_YOUTUBE_PY} dose not exist.')
                sys.exit()
            command = "which python3"
            p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
            PYTHON_CMD = p.communicate()[0].rstrip()
            if "python3" not in PYTHON_CMD :
                root_logger.critical("Err. python3 not installed..")
                sys.exit()
            root_logger.critical(f'PYTHON_CMD = {PYTHON_CMD}')
            SAVED_DIR = os.getenv("SAVE_DIR", "/mnt/recordings/saved")
            root_logger.critical(f'SAVED_DIR = {SAVED_DIR}')
            UPLOADED_DIR = os.getenv("UPLOADED_DIR", "/mnt/recordings/uploaded")
            root_logger.critical(f'UPLOADED_DIR = {UPLOADED_DIR}')
            WARN_USAGE = configs['WARN_USAGE']
            root_logger.critical(f'WARN_USAGE = {WARN_USAGE}')
            PIPE_FLAG = configs["PIPE_FLAG"]
            root_logger.critical(f'PIPE_FLAG = {PIPE_FLAG}')
    else :
        root_logger.critical(f"{CONFIG_PATH} is not exist. Configuration file is required.")
        sys.exit()

# container가 아닌 경우
else :
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH) as json_file:
            configs = json.load(json_file)

            root_logger.critical('=== CONFIGURATIONS LOADED ===')
            try :
                INTERVAL = float(configs['INTERVAL'])
            except KeyError :
                INTERVAL = 5
            root_logger.critical(f'INTERVAL = {INTERVAL}')   

            try :
                QUALITY = configs['QUALITY']
            except KeyError :
                QUALITY = 'best'
            root_logger.critical(f'QUALITY = {QUALITY}')

            try :
                OUTPUT_DIR = configs['OUTPUT_DIR']
            except KeyError :
                OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/mnt/recordings")
            root_logger.critical(f'OUTPUT_DIR = {OUTPUT_DIR}')
            
            try :
                SAVED_DIR = configs['SAVED_DIR']
            except KeyError :
                SAVED_DIR = os.getenv("SAVE_DIR", "/mnt/recordings/saved")
            root_logger.critical(f'SAVED_DIR = {SAVED_DIR}')

            try :
                UPLOADED_DIR = configs['UPLOADED_DIR']
            except KeyError :
                UPLOADED_DIR = os.getenv("UPLOADED_DIR", "/mnt/recordings/uploaded")
            root_logger.critical(f'UPLOADED_DIR = {UPLOADED_DIR}')

            try :
                FILE_RULE = configs['FILE_RULE']
            except KeyError :
                FILE_RULE = "[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts"
            root_logger.critical(f'FILE_RULE = {FILE_RULE}')

            try :
                TARGET_URL = configs['TARGET_URL']
            except KeyError :
                TARGET_URL = os.path.join(ROOT_DIR, "target_url.txt")
            root_logger.critical(f'TARGET_URL = {TARGET_URL}')

            try :
                STREAMLINK_CMD = configs['STREAMLINK_CMD']
            except KeyError :
                command = "which streamlink"
                p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
                STREAMLINK_CMD = p.communicate()[0].rstrip()
                if "streamlink" not in STREAMLINK_CMD :
                    root_logger.critical("Err. streamlink not installed..")
                    sys.exit()
            root_logger.critical(f'STREAMLINK_CMD = {STREAMLINK_CMD}')

            try :
                STREAMLINK_OPTIONS = configs['STREAMLINK_OPTIONS']
            except KeyError :
                STREAMLINK_OPTIONS = "--force --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns"
            root_logger.critical(f'STREAMLINK_OPTIONS = {STREAMLINK_OPTIONS}')

            try :
                STREAMLINK_LOG_OPTIONS = configs['STREAMLINK_LOG_OPTIONS']
            except KeyError :
                STREAMLINK_LOG_OPTIONS = "info"
            root_logger.critical(f'STREAMLINK_LOG_OPTIONS = {STREAMLINK_LOG_OPTIONS}')

            try :
                STREAMLINK_LOG_PATH = configs['STREAMLINK_LOG_PATH']
            except KeyError :
                STREAMLINK_LOG_PATH = os.path.join(ROOT_DIR, "logs/streamlink")
            root_logger.critical(f'STREAMLINK_LOG_PATH = {STREAMLINK_LOG_PATH}')

            try :
                UPLOAD_YOUTUBE_PY = configs['UPLOAD_YOUTUBE_PY']
            except KeyError :
                UPLOAD_YOUTUBE_PY = os.path.join(ROOT_DIR, "src/upload_youtube.py")
            root_logger.critical(f'UPLOAD_YOUTUBE = {UPLOAD_YOUTUBE_PY}')
            if not os.path.isfile(UPLOAD_YOUTUBE_PY):
                root_logger.critical(f'Err. {UPLOAD_YOUTUBE_PY} dose not exist.')
                sys.exit()

            try :
                PYTHON_CMD = configs['PYTHON_CMD']
            except KeyError :
                command = "which python3"
                p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
                PYTHON_CMD = p.communicate()[0].rstrip()
                if "python3" not in PYTHON_CMD :
                    root_logger.critical("Err. python3 not installed..")
                    sys.exit()
            root_logger.critical(f'PYTHON_CMD = {PYTHON_CMD}')

            try :
                WARN_USAGE = int(configs['WARN_USAGE'])
            except KeyError :
                WARN_USAGE = 70
            root_logger.critical(f'WARN_USAGE = {WARN_USAGE}')
            
            PIPE_FLAG = False
            root_logger.critical(f'PIPE_FLAG = {PIPE_FLAG}')
    else :
        root_logger.critical(f"{CONFIG_PATH} is not exist. Configuration file is required.")
        sys.exit()


''' Private Configuration '''
if SYS_PLATFORM == 'Windows':
    SECRETS_PATH = os.path.join(ROOT_DIR, r'config\secrets.json')
else :
    SECRETS_PATH = os.path.join(ROOT_DIR, 'config/secrets.json')

FROM_EMAIL_ADDR = ""
TO_EMAIL_ADDR = ""
if os.path.isfile(SECRETS_PATH):
    with open(SECRETS_PATH) as json_file:
        sec = json.load(json_file)

        root_logger.critical('=== PRIVATE LOADED ===')
        try :
            FROM_EMAIL_ADDR = sec['FROM_EMAIL_ADDR']
            TO_EMAIL_ADDR = sec['TO_EMAIL_ADDR']
        except KeyError :
            root_logger.critical(f"No mail Address in {SECRETS_PATH}. Don't send email")
        try :
            SLACK_CHANNEL = configs["SLACK_CHANNEL"]
            root_logger.critical(f'SLACK_CHANNEL = {SLACK_CHANNEL}')
        except KeyError :
            SLACK_CHANNEL = "streamlink-alarm"
        try :
            SLACK_KEY = sec['SLACK_KEY']
            root_logger.critical(f'Loaded SLACK_KEY')
        except KeyError :
            root_logger.critical(f"No SLACK KEY.")
else :
    root_logger.critical(f"No {SECRETS_PATH}. Don't send email")
    


''' Youtube Upload Secrets '''
if SYS_PLATFORM == 'Windows':
    CLIENT_SEC_PATH = os.path.join(ROOT_DIR, r'src\client_secrets.json')
    OAUTH_PATH = os.path.join(ROOT_DIR, r'src\upload_youtube.py-oauth2.json')
else :
    CLIENT_SEC_PATH = os.path.join(ROOT_DIR, 'src/client_secrets.json')
    OAUTH_PATH = os.path.join(ROOT_DIR, 'src/upload_youtube.py-oauth2.json')

if os.path.isfile(CLIENT_SEC_PATH) == False :
    root_logger.critical(f"No client_secrets.json. check volumn")
    sys.exit()
    
if os.path.isfile(OAUTH_PATH) == False :
    root_logger.critical(f"No upload_youtube.py-oauth2.json. check volumn")
    sys.exit()
