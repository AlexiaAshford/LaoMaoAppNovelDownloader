import os
import re
from .HttpUtil import Util
from instance import *
from .AesDecrypt import *
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor

Vars.cfg.save()


class Download():
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.novel_intro = ""
        self.max_worker = Vars.cfg.data.get('max_workers_number')
        self.getUtil = Util().get

    def filedir(self):
        meragefiledir = os.path.join(
            'config', self.bookName)  # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(meragefiledir)
        filenames.sort(key=lambda x: int(x.split('.')[0]))
        file = open(os.path.join(
            'Download', f'{self.bookName}.txt'), 'a', encoding='utf-8')
        for filename in filenames:  # 先遍历文件名
            filepath = os.path.join(meragefiledir, filename)
            #遍历单个文件，读取行数
            for line in open(filepath, encoding='utf-8'):
                file.writelines(line)
            file.write('\n')
        file.close()

    def write_txt(self, content_chap_title, chapter_list, number):  # 将信息写入TXT文件
        """删去windowns不规范字符"""
        chapter_list = re.sub(r'[？?\*|“<>:/]', '', chapter_list)
        with open(os.path.join('config', self.bookName, f"{number}.{chapter_list}.txt"), 'w', encoding='utf-8', newline='') as fb:
            fb.write(str(content_chap_title))

    def ThreadPool_download(self, urls, number):
        """多线程下载函数"""
        content = self.getUtil(urls)['data']
        book_title = self.chapter_list[number-1]
        """跳过屏蔽章节"""
        if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
            print(book_title)
            content_title = "\n\n{}\n{}".format(book_title, content_(content))
            self.write_txt(content_title, book_title, number)
        else:
            print("{}这是屏蔽章节，跳过下载".format(book_title))

    def SearchBook(self, bookname):
        urls = ['https://api.laomaoxs.com/Search/index?key={}&page={}'.format(
            bookname, i) for i in range(100)]
        for url in urls:
            if not self.getUtil(url)['data']:
                print('获取完毕')
                break
            """存储bookid进列表中"""
            search_book = [data['book_id']
                           for data in self.getUtil(url)['data']]
        return search_book

    def class_list(self, Tag_Number):
        class_list_bookid = []
        for i in range(10000):
            url = f'https://api.laomaoxs.com/novel/lists?order=0&status=0&sex=1&page={i}&type={Tag_Number}'
            if not self.getUtil(url)['data']:
                print('排行榜已经下载完毕')
                break
            for data in self.getUtil(url)['data']:
                self.bookName = data['book_title']
                bookid = str(data['book_id'])
                print(self.bookName)
                class_list_bookid.append(bookid)
            print(class_list_bookid[-1])
        return class_list_bookid

    def ranking(self):
        ranking_list_bookid = []
        for i in range(10000):
            url = f'https://api.laomaoxs.com/novel/ranking?sex=2&page={i}&order=0'
            if not self.getUtil(url)['data']:
                print('分类已经下载完毕')
                break
            for data in self.getUtil(url)['data']:
                self.bookName = data['book_title']
                print(self.bookName)
                ranking_list_bookid.append(data['book_id'])
        return ranking_list_bookid

    def ThreadPool(self, chapters_url_list, BOOK_INFO_LIST):
        BOOK_INFO_LIST = BOOK_INFO_LIST[0]
        self.bookid = BOOK_INFO_LIST.get('book_id')
        self.bookName = BOOK_INFO_LIST.get('book_title')
        self.novel_intro = BOOK_INFO_LIST.get('book_desc')
        self.authorName = BOOK_INFO_LIST.get('book_author')
        self.chapter_list = BOOK_INFO_LIST.get('chapter_list')
        self.lastUpdateTime = BOOK_INFO_LIST.get('update_time')
        self.book_type = BOOK_INFO_LIST.get('book_type')
        self.isFinish = BOOK_INFO_LIST.get('book_status')
        """多线程并发实现"""
        with ThreadPoolExecutor(max_workers=self.max_worker) as t:
            for number, book_url in enumerate(chapters_url_list):
                t.submit(self.ThreadPool_download, book_url, number)

        with open(os.path.join("Download", self.bookName + '.txt'), 'w') as f:
            self.filedir()
            print(f'\n小说 {self.bookName} 下载完成')
