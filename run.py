import fire
from instance import *
from API import LaoMaoxsAPI
from API import Settings


def book(bookid):
    Download.GetBook(bookid)
    if Vars.cfg.data.get('Open_ThreadPool'):
        Download.ThreadPool(Vars.cfg.data.get('max_workers_number'))
    else:
        Download.chapters(pool=False)


def login(user_info):
    usernames, passwords = (
        str(user_info).split(',')[0], 
        str(user_info).split(',')[1])
    from API.login import Login
    Login(usernames, passwords).Login_account()


def maxs(max):
    if str(max).isdigit():
        max_workers_number = 12 if int(max) > 12 else int(max)
        Vars.cfg.data['max_workers_number'] = max_workers_number
        print("线程已经设置为", Vars.cfg.data.get('max_workers_number'))
        Vars.cfg.save()
    else:
        print(max, "不是数字，请重新输入")


def name(name):
    search_book = Download.SearchBook(name)
    for i in search_book:
        Download.GetBook(i)
        if Vars.cfg.data.get('Open_ThreadPool'):
            print("开启多线程")
            Download.ThreadPool(Vars.cfg.data.get('max_workers_number'))
        else:
            Download.chapters(pool=False)


def tag(tag):
    for i in Download.class_list(tag):
        Download.GetBook(i)
        if Vars.cfg.data.get('Open_ThreadPool'):
            Download.ThreadPool(Vars.cfg.data.get('max_workers_number'))
        else:
            Download.chapters(pool=False)


def rank():
    for i in Download.ranking():
        Download.GetBook(i)
        if Vars.cfg.data.get('Open_ThreadPool'):
            Download.ThreadPool(Vars.cfg.data.get('max_workers_number'))
        else:
            Download.chapters(pool=False)
def help():
    print(Vars.cfg.data.get('help'))
    

if __name__ == '__main__':
    Vars.cfg.load()
    Settings.setup_config()
    Download = LaoMaoxsAPI.Download()
    fire.Fire()
