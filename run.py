import fire
import book
from instance import *
from API import LaoMaoxsAPI, Settings, HttpUtil, userlogin, UrlConstants

class Shell(object):
    def id(self, bookid=None):
        if bookid is None:
            bookid = get('请输入Bookid:').strip()
        if str(bookid).isdigit():
            book_info_url = UrlConstants.BOOK_INDEX.format(bookid)
            book.BOOK(HttpUtil.get(book_info_url)).book_show()
        else:
            print('输入内容不是数字')


    def login(self, usernames=None, passwords=None):
        user_setting = False
        if usernames != None and passwords != None:
            if len(str(usernames)) <= 6:
                print("账号不能小于6位!")
                usernames, user_setting= None, False
            if len(str(passwords)) <= 6:
                print("密码不能小于6位!")
                passwords. user_setting= None, False
            else:
                user_setting = True
        if usernames is None:
            usernames  = get('请输入usernames:').strip()
            while len(str(usernames)) <= 6:
                print("账号不能小于6位!")
                usernames  = get('请输入usernames:').strip()
            else:
                user_setting = True
        if passwords is None:
            passwords  = get('请输入passwords:').strip()
            while len(str(passwords)) <= 6:
                print("密码不能小于6位!")
                passwords  = get('请输入passwords:').strip()
            else:
                user_setting = True
        if user_setting or user_setting is True:
            userlogin.Login(usernames, passwords).Login_account()

    def max(self, max_num=None):
        if max_num is None:
            max_num = get('请输入线程数目:').strip()
        if str(max_num).isdigit():
            max_workers_number = 12 if int(max_num) > 12 else int(max_num)
            Vars.cfg.data['max_workers_number'] = max_workers_number
            print("线程已经设置为", Vars.cfg.data.get('max_workers_number'))
            Vars.cfg.save()
        else:
            print(max_num, "不是数字！")


    def name(self, bookName=None):
        if bookName is None:
            bookName = get('请输入bookName:').strip()
            search_bookid_list = Download.SearchBook(bookName)
        else:
            search_bookid_list = Download.SearchBook(bookName)
        for bookid in search_bookid_list:
            book_info_url = UrlConstants.BOOK_INDEX.format(bookid)
            book.BOOK(HttpUtil.get(book_info_url)).book_show()


    def tag(self, tag):
        if tag is None:
            tag = get('请输入tag:').strip()
        for bookid in Download.class_list(tag):
            book_info_url = UrlConstants.BOOK_INDEX.format(bookid)
            book.BOOK(HttpUtil.get(book_info_url)).book_show()


    def rank(self):
        for bookid in Download.ranking():
            book_info_url = UrlConstants.BOOK_INDEX.format(bookid)
            book.BOOK(HttpUtil.get(book_info_url)).book_show()


    def help(self):
        print(Vars.cfg.data.get('help'))


if __name__ == '__main__':
    Vars.cfg.load()
    Settings.setup_config()
    Download = LaoMaoxsAPI.Download()
    fire.Fire(Shell)
