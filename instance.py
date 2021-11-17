from config import *


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

def content_(content):
    import re
    return ''.join([re.sub(r'^\s*', "\n　　", content)
        for content in content.split("\n") if re.search(r'\S', content) != None])