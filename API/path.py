from instance import *

def SAVE_FILE(bookName, number, book_title)
    return os.path.join(Vars.cfg.data.get('save_dir'), bookName, f"{}.{}.txt"),

def OUT_FILE(bookName)
    return os.path.join(Vars.cfg.data.get('output_dir'), f'{bookName}.txt'), 'a', line)
