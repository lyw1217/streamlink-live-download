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
elif SYS_PLATFORM == 'Windows':
    LOGGING_PATH = os.path.join(ROOT_DIR, 'config\logging.json')
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

''' Main Configuration '''
if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')
elif SYS_PLATFORM == 'Windows':
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config\config.json')

with open(CONFIG_PATH) as json_file:
    configs = json.load(json_file)
    f_send = {}

    root_logger.critical('=== CONFIGURATIONS ===')
    INTERVAL = float(configs['INTERVAL'])
    root_logger.critical(f'INTERVAL = {INTERVAL}')
    QUALITY = configs['QUALITY']
    root_logger.critical(f'QUALITY = {QUALITY}')
    OUTPUT_DIR = configs['OUTPUT_DIR']
    root_logger.critical(f'OUTPUT_DIR = {OUTPUT_DIR}')
    FILE_RULE = configs['FILE_RULE']
    root_logger.critical(f'FILE_RULE = {FILE_RULE}')
    TARGET_URL = configs['TARGET_URL']
    root_logger.critical(f'TARGET_URL = {TARGET_URL}')
    STREAMLINK_CMD = configs['STREAMLINK_CMD']
    root_logger.critical(f'STREAMLINK_CMD = {STREAMLINK_CMD}')
    STREAMLINK_OPTIONS = configs['STREAMLINK_OPTIONS']
    root_logger.critical(f'STREAMLINK_OPTIONS = {STREAMLINK_OPTIONS}')
    STREAMLINK_LOG_OPTIONS = configs['STREAMLINK_LOG_OPTIONS']
    root_logger.critical(f'STREAMLINK_LOG_OPTIONS = {STREAMLINK_LOG_OPTIONS}')
    STREAMLINK_LOG_PATH = configs['STREAMLINK_LOG_PATH']
    root_logger.critical(f'STREAMLINK_LOG_PATH = {STREAMLINK_LOG_PATH}')
