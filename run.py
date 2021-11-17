import fire
import book
from instance import *
from API import LaoMaoxsAPI, Settings, HttpUtil, userlogin

class Shell(object):
    def id(self, bookid):
        if str(bookid).isdigit():
            book_info_url = 'https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(
                bookid)
            book.BOOK(HttpUtil.Util().get(book_info_url)).book_show()
        else:
            print('输入内容不是数字')


    def login(self, usernames, passwords):
        userlogin.Login(usernames, passwords).Login_account()


    def maxs(self, max):
        if str(max).isdigit():
            max_workers_number = 12 if int(max) > 12 else int(max)
            Vars.cfg.data['max_workers_number'] = max_workers_number
            print("线程已经设置为", Vars.cfg.data.get('max_workers_number'))
            Vars.cfg.save()
        else:
            print(max, "不是数字，请重新输入")


    def name(self, name):
        search_book = Download.SearchBook(name)
        for bookid in search_book:
            book_info_url = 'https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(
                bookid)
            book.BOOK(HttpUtil.Util().get(book_info_url)).book_show()


    def tag(self, tag):
        for bookid in Download.class_list(tag):
            book_info_url = 'https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(
                bookid)
            book.BOOK(HttpUtil.Util().get(book_info_url)).book_show()


    def rank(self):
        for bookid in Download.ranking():
            book_info_url = 'https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(
                bookid)
            book.BOOK(HttpUtil.Util().get(book_info_url)).book_show()


    def help(self):
        print(Vars.cfg.data.get('help'))


if __name__ == '__main__':
    Vars.cfg.load()
    Settings.setup_config()
    Download = LaoMaoxsAPI.Download()
    fire.Fire(Shell)
