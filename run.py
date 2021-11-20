import fire
import book
from instance import *
from function import Search, userlogin, Category
from API import LaoMaoxsAPI, Settings, HttpUtil, UrlConstants

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
        # if usernames != None and passwords != None:
        #     if len(str(usernames)) <= 6:
        #         print("账号不能小于6位!")
        #         usernames, user_setting = None, False
        #     if len(str(passwords)) <= 6:
        #         print("密码不能小于6位!")
        #         passwords. user_setting = None, False
        #     else:
        #         user_setting = True
        if usernames is None or len(str(usernames)) <= 6:
            usernames  = get('请输入usernames:').strip()
            while len(str(usernames)) <= 6:
                print("账号不能小于6位!")
                usernames = get('请输入usernames:').strip()
        if passwords is None or len(str(passwords)) <= 6:
            passwords  = get('请输入passwords:').strip()
            while len(str(passwords)) <= 6:
                print("密码不能小于6位!")
                passwords  = get('请输入passwords:').strip()
        else:
            userlogin.Login(usernames, passwords).Login_account()
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
        search_result_url_list = [
            UrlConstants.SERCH_BOOK.format(bookName, i) for i in range(20)]
        
        for list_num, url in enumerate(search_result_url_list):
            Search_ = Search.SearchBooks(url)
            if Search_.test_data_list() == 200:
                print(f'开始下载第{list_num}页')
                Search_.get_seach_info()
            elif Search_.test_data_list() == 0:
                print('已下载完所有搜索的书籍')
                return 
            elif Search_.test_data_list() == 404:
                print('搜结果不存在这本书！')
        #     search_bookid_list = Download.SearchBook(bookName)
        # else:
        #     search_bookid_list = Download.SearchBook(bookName)
        # for bookid in search_bookid_list:
        #     book_info_url = UrlConstants.BOOK_INDEX.format(bookid)
        #     book.BOOK(HttpUtil.get(book_info_url)).book_show()


    def tag(self, Categor_num=None):
        if Categor_num is None:
            Categor_num = get('请输入tag:').strip()
        
        Categor_url_list = [UrlConstants.CATEGOR_URL.format(
            i, Categor_num) for i in range(10000)]
        for list_num, Categor_url in enumerate(Categor_url_list):
            Category_ = Category.Categorys(Categor_url)
            if Category_.test() == 200:
                print(f'开始下载第{list_num}页')
                Category.Categorys(Categor_url).Category_download()
            elif Category_.test() == 0:
                print('分类已经下载完毕')
                return
            elif Category_.test() == 404:
                print('获取失败')


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
