from API import HttpUtil, UrlConstants
from book import BOOK
from instance import *


class Categorys(object):
    def __init__(self, Categor_url):
        self.Categor_info = HttpUtil.get(Categor_url)
        self.Categor_code = self.Categor_info.get('code')
        self.Categor_msg = self.Categor_info.get('msg')
        self.Categor_data = self.Categor_info.get('data')

    def test(self):
        if self.Categor_info.get('code') == 1:
            if self.Categor_info is not None:
                # print(self.Categor_data)
                return 200
            else:
                return 0
        else:
            print(self.Categor_msg, '获取失败')
            return 404

    def Category_download(self):
        for Categor_data_info in self.Categor_data:
            book_id = Categor_data_info.get('book_id')
            book_status = Categor_data_info.get('book_status')
            book_type = Categor_data_info.get('book_type')
            book_desc = Categor_data_info.get('book_desc')
            chapter_count = Categor_data_info.get('chapter_count')
            book_hits = Categor_data_info.get('book_hits')
            BOOK(HttpUtil.get(UrlConstants.BOOK_INDEX.format(book_id))).book_show()

    # def class_list(self):
    #     class_list_bookid = []
    #     for Categor_url in self.Categor_url_list:
    #         if not HttpUtil.get(Categor_url).get('data'):
    #             print('排行榜已经下载完毕')
    #             break
    #         for data in HttpUtil.get(Categor_url)['data']:
    #             self.bookName = data['book_title']
    #             bookid = str(data['book_id'])
    #             print(self.bookName)
    #             class_list_bookid.append(bookid)
    #         print(class_list_bookid[-1])
    #     return class_list_bookid
