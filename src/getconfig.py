import os
import json
import platform
import logging
import logging.config
import subprocess as sp

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
SYS_PLATFORM = platform.system()

''' Logging Configuration '''
if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config/logging.json')
elif SYS_PLATFORM == 'Windows':
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config\logging.json')
else :
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config/logging.json')
if os.path.isfile(LOGGING_PATH):
    with open(LOGGING_PATH) as json_file:
        log_configs = json.load(json_file)
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
    exit()



''' Main Configuration '''
if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')
elif SYS_PLATFORM == 'Windows':
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config\config.json')
else :
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')

IS_CONTAINER = os.getenv("IS_CONTAINER", "")
# container 인 경우
if len(IS_CONTAINER) > 0 :
    root_logger.critical('=== CONFIGURATIONS LOADED ===')
    INTERVAL = 5
    root_logger.critical(f'INTERVAL = {INTERVAL}')   
    QUALITY = 'best'
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
        exit()
    root_logger.critical(f'STREAMLINK_CMD = {STREAMLINK_CMD}')
    STREAMLINK_OPTIONS = "--force --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns"
    root_logger.critical(f'STREAMLINK_OPTIONS = {STREAMLINK_OPTIONS}')
    STREAMLINK_LOG_OPTIONS = "info"
    root_logger.critical(f'STREAMLINK_LOG_OPTIONS = {STREAMLINK_LOG_OPTIONS}')
    STREAMLINK_LOG_PATH = os.path.join(ROOT_DIR, "logs/streamlink")
    root_logger.critical(f'STREAMLINK_LOG_PATH = {STREAMLINK_LOG_PATH}')
    UPLOAD_YOUTUBE_PY = os.path.join(ROOT_DIR, "src/upload_youtube.py")
    root_logger.critical(f'UPLOAD_YOUTUBE = {UPLOAD_YOUTUBE_PY}')
    command = "which python3"
    p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
    PYTHON_CMD = p.communicate()[0].rstrip()
    if "python3" not in PYTHON_CMD :
        root_logger.critical("Err. python3 not installed..")
        exit()
    root_logger.critical(f'PYTHON_CMD = {PYTHON_CMD}')
    SAVED_DIR = os.getenv("SAVE_DIR", "/mnt/recordings/saved")
    root_logger.critical(f'SAVED_DIR = {SAVED_DIR}')
    WARN_USAGE = 85
    root_logger.critical(f'WARN_USAGE = {WARN_USAGE}')

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
                    exit()
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

            try :
                PYTHON_CMD = configs['PYTHON_CMD']
            except KeyError :
                command = "which python3"
                p = sp.Popen(command.split(' '), stdout=sp.PIPE, text=True)
                PYTHON_CMD = p.communicate()[0].rstrip()
                if "python3" not in PYTHON_CMD :
                    root_logger.critical("Err. python3 not installed..")
                    exit()
            root_logger.critical(f'PYTHON_CMD = {PYTHON_CMD}')

            try :
                SAVED_DIR = configs['SAVED_DIR']
            except KeyError :
                SAVED_DIR = os.getenv("SAVE_DIR", "/mnt/recordings/saved")
            root_logger.critical(f'SAVED_DIR = {SAVED_DIR}')

            try :
                WARN_USAGE = int(configs['WARN_USAGE'])
            except KeyError :
                WARN_USAGE = 85
            root_logger.critical(f'WARN_USAGE = {WARN_USAGE}')
    else :
        root_logger.critical(f"{CONFIG_PATH} is not exist. Configuration file is required.")
        exit()


''' Private Configuration '''
if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    SECRETS_PATH = os.path.join(ROOT_DIR, 'config/secrets.json')
elif SYS_PLATFORM == 'Windows':
    SECRETS_PATH = os.path.join(ROOT_DIR, 'config\secrets.json')
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
else :
    root_logger.critical(f"No {SECRETS_PATH}. Don't send email")
    


