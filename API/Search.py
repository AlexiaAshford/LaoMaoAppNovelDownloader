
from instance import *
from API import LaoMaoxsAPI, Settings, HttpUtil, userlogin, UrlConstants


class SearchBooks:


    def SearchBook(self, bookname):
        urls = [UrlConstants.SERCH_BOOK.format(
            bookname, i) for i in range(100)]
            
        # print(url)
        for url in urls:
            if not HttpUtil.get(url)['data']:
                break
            """存储bookid进列表中"""
            search_book = [data['book_id']
                           for data in HttpUtil.get(url)['data']]
        return search_book
