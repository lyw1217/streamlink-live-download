import os
import json
import platform
import logging
import logging.config

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
SYS_PLATFORM = platform.system()

''' Logging Configuration '''
if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config/logging.json')
elif SYS_PLATFORM == 'Windows' :
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config\logging.json')
with open(LOGGING_PATH) as json_file :
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

''' Main Configuration '''
if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')
elif SYS_PLATFORM == 'Windows' :
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config\config.json')

with open(CONFIG_PATH) as json_file :
    configs = json.load(json_file)
    f_send = {}

    INTERVAL = int(configs['INTERVAL'])
    print(INTERVAL)
    QUALITY = configs['QUALITY']
    print(QUALITY)
    OUTPUT_DIR = configs['OUTPUT_DIR']
    print(OUTPUT_DIR)
    FILE_RULE = configs['FILE_RULE']
    print(FILE_RULE)
    TARGET_URL = configs['TARGET_URL']
    print(TARGET_URL)
    STREAMLINK_CMD = configs['STREAMLINK_CMD']
    print(STREAMLINK_CMD)
    STREAMLINK_OPTIONS = configs['STREAMLINK_OPTIONS']
    print(STREAMLINK_OPTIONS)
    STREAMLINK_LOG_OPTIONS = configs['STREAMLINK_LOG_OPTIONS']
    print(STREAMLINK_LOG_OPTIONS)
    STREAMLINK_LOG_PATH = configs['STREAMLINK_LOG_PATH']
    print(STREAMLINK_LOG_PATH)