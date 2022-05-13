import os
import platform

from getconfig import *

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
SYS_PLATFORM = platform.system()

if SYS_PLATFORM == 'Linux' or SYS_PLATFORM == 'Drawin':
    FIFO_FILENAME = os.path.join(ROOT_DIR, 'fifo-pystream')
elif SYS_PLATFORM == 'Windows':
    FIFO_FILENAME = os.path.join(ROOT_DIR, 'fifo-pystream')
else :
    FIFO_FILENAME = os.path.join(ROOT_DIR, 'fifo-pystream')

def create_pipe():
    if not os.path.exists(FIFO_FILENAME):
        print("create pipe...")
        os.mkfifo(FIFO_FILENAME)
    write_pipe("date")

def write_pipe(cmd):
    if os.path.exists(FIFO_FILENAME):
        root_logger.critical(f"writing to pipe... > {cmd}")
        with open(FIFO_FILENAME, "w") as fp_fifo:
            fp_fifo.write(cmd)
    else :
        root_logger.critical("dose not exist pipe...")

def recv_pipe():
    with open(FIFO_FILENAME, "r") as fifo:
        data = fifo.read()
    
    return data 
