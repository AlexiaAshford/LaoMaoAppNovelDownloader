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
        self.charCount = ""
        self.authorName = ""
        self.chapter_list = []
        self.os_config_json = os.path.join(os.getcwd(), 'config')
        self.lastUpdateTime = ""
        self.getUtil = Util().get

    # def inputs(self, name):
    #     inp = input(name)
    #     while not inp:
    #         inp = input(name)
    #     else:
    #         return inp

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

    def os_file(self):
        self.main_path = os.getcwd()  # 项目路径
        # 创建Download文件夹
        self.os_novel_download = os.path.join(self.main_path, "Download")
        if not os.path.exists(self.os_novel_download):
           os.mkdir(self.os_novel_download)
           print(f'已在{self.main_path}创建Download文件夹')

        # 创建config_json文件夹
        if not os.path.exists(self.os_config_json):
           os.mkdir(self.os_config_json)
           print(f'已在{self.main_path}创建config文件夹')

        if not os.path.exists(os.path.join('config', self.bookName)):
            os.makedirs(os.path.join('config', self.bookName))

        # 创建list文本
        if not (os.path.join(self.main_path, "list.txt")):
           file = open(os.path.join(self.main_path, "list.txt"),
                       'a', encoding='utf-8')

        # 创建txt文本
        if not os.path.exists(os.path.join(self.os_novel_download, f"{self.bookName}.txt")):
            open(os.path.join(self.os_novel_download,
                        f"{self.bookName}.txt"), "a", encoding='utf-8')

    def write_txt(self, content_chap_title, chapter_list, number):  # 将信息写入TXT文件
        """删去windowns不规范字符"""
        chapter_list = re.sub(r'[？?\*|“<>:/]', '', chapter_list)
        with open(os.path.join('config', self.bookName, f"{number}.{chapter_list}.txt"), 'w', encoding='utf-8', newline='') as fb:
            fb.write(str(content_chap_title))

    def read_config_name(self):
        # config读取文件名
        read_name = os.listdir(os.path.join('config', self.bookName))
        return read_name

    def GetBook(self, bookid):
        self.bookid = bookid
        url = 'https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(
            self.bookid)
        info_book = self.getUtil(url)['data']
        # print(info_book)
        self.novel_intro = info_book['book_desc']
        self.lastUpdateTime = info_book['update_time']
        self.bookName = info_book['book_title']
        self.authorName = info_book['book_author']
        book_type = info_book['book_type']
        self.isFinish = info_book['book_status']
        self.chapter_list = info_book['chapter_list']
        print("\n\n书名:{}\n序号:{}\n作者:{}\n分类:{}".format(
            self.bookName, self.bookid, self.authorName, book_type))
        print("简介:{}\n更新时间:{}\n{}".format(
            self.novel_intro, self.lastUpdateTime, self.isFinish))
        """建立文件夹和文件"""
        self.os_file()

    def chapters(self, Open_ThreadPool):
        chapters_list = []
        print('开始下载{} ,一共{}章'.format(self.bookName, len(self.chapter_list)))
        if Open_ThreadPool:
            for n, i in enumerate(range(len(self.chapter_list))):
                """跳过已经下载的章节"""
                if self.chapter_list[n] in ''.join(self.read_config_name()):
                    print(self.chapter_list[n], '已经下载过')
                    continue
                num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
                chapters_list.append('https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'.format(
                    num, self.bookid, i))
            return chapters_list
        if not Open_ThreadPool:
            for n, i in enumerate(track(range(len(self.chapter_list)))):
                num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
                book_title = self.chapter_list[n]
                """跳过已经下载的章节"""
                if self.chapter_list[n] in ''.join(self.read_config_name()):
                    print(self.chapter_list[n], '已经下载过')
                    continue
                url = 'https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'.format(
                    num, self.bookid, i)
                content = self.getUtil(url)['data']
                """跳过屏蔽章节"""
                if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
                    print(book_title)
                    content = ''.join([re.sub(r'^\s*', "\n　　", content)
                                      for content in content.split("\n") if re.search(r'\S', content) != None])
                    content_chap_title = f"\n\n{book_title}\n{content}"
                    self.write_txt(content_chap_title, book_title, n)
                else:
                    print(f"{self.chapter_list[n]}这是屏蔽章节，跳过下载")
            with open(os.path.join("Download", self.bookName + '.txt'), 'w') as f:
                self.filedir()
                print(f'\n小说 {self.bookName} 下载完成')

    def ThreadPool_download(self, urls, number):
        """多线程下载函数"""
        content = self.getUtil(urls)['data']
        book_title = self.chapter_list[number-1]
        # print(content)
        """跳过屏蔽章节"""
        if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
            print(book_title)
            content = ''.join([re.sub(r'^\s*', "\n　　", content)
                              for content in content.split("\n") if re.search(r'\S', content) != None])
            content_chap_title = f"\n\n{book_title}\n{content}"
            self.write_txt(content_chap_title, book_title, number)
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
            search_book = [data['book_id'] for data in self.getUtil(url)['data']]
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

    def ThreadPool(self, max_workers_number):
        """多线程并发实现"""
        with ThreadPoolExecutor(max_workers=max_workers_number) as t:
            for number, book_url in enumerate(self.chapters(True)):
                new_thread = t.submit(
                    self.ThreadPool_download, book_url, number)
        with open(os.path.join("Download", self.bookName + '.txt'), 'w') as f:
            self.filedir()
            print(f'\n小说 {self.bookName} 下载完成')
