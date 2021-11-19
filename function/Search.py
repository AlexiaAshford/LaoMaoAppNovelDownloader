
from instance import *
from API import HttpUtil, UrlConstants
import book


class SearchBooks:

    def __init__(self, url):
        self.search_url = url
        self.search_info = HttpUtil.get(self.search_url)
        self.search_info_msg = self.search_info.get('msg')
        self.search_info_code = self.search_info.get('code')
        self.search_info_data = self.search_info.get('data')
        self.book_id_list = list()

    def test_data_list(self):
        if self.search_info_msg == 'OK':
            if self.search_info_data is not None:
                self.get_seach_info()
                return True
            else:
                return False

    def get_seach_info(self):
        for info_data in self.search_info_data:
            book_id = info_data.get('book_id')
            book_status = info_data.get('book_status')
            book_type = info_data.get('book_type')
            book_desc = info_data.get('book_desc')
            chapter_count = info_data.get('chapter_count')
            book_hits = info_data.get('book_hits')
            self.book_id_list.append(book_id)
            book.BOOK(
                HttpUtil.get(UrlConstants.BOOK_INDEX.format(book_id))
            ).book_show()

        # if not self.search_info_data:
        #     return

        # for url in book_info_url_list:
        #     if not HttpUtil.get(url)['data']:
        #         break
        #     """存储bookid进列表中"""
        #     search_book = [data['book_id']
        #                    for data in HttpUtil.get(url)['data']]
        # return search_book
