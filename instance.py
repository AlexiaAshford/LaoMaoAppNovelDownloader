from config import *
import os
import re
import time

class Vars:
    cfg = Config('Config.json', os.getcwd())
    current_bookshelf = None
    current_book = None


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default

def del_title(title):
    """删去windowns不规范字符"""
    return re.sub(r'[？?\*|“<>:/]', '', title)

def content_(content):
    return ''.join([re.sub(r'^\s*', "\n　　", content)
        for content in content.split("\n") if re.search(r'\S', content) != None])
    
def write(PATH, mode, info=None):
    if info is not None:
        try:
            with open(PATH, f'{mode}', encoding='UTF-8', newline='') as file:
                file.writelines(info)
        except (UnicodeEncodeError, UnicodeDecodeError)as e:
            print(e)
            with open(PATH, f'{mode}', encoding='gbk', newline='') as file:
                file.writelines(info)
    else:
        try:
            file =  open(PATH, f'{mode}', encoding='UTF-8')
            return file
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(e)
            file =  open(PATH, f'{mode}', encoding='gbk')
            return file