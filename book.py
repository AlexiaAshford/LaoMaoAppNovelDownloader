import os
from instance import *
from API.LaoMaoxsAPI import Download

class BOOK:

    def __init__(self, BOOK_INFO):
        self.BOOK_INFO = BOOK_INFO
        self.chapterurl = 'https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'


    def config_bookname(self):
        return os.listdir(os.path.join('config', self.bookName))
    
    def get_book_info(self):
        self.BOOK_INFO_LIST = []
        if self.BOOK_INFO.get('msg') == 'ok':
            Book_Data = self.BOOK_INFO.get('data')
            self.bookid = Book_Data.get('book_id')
            self.bookName = Book_Data.get('book_title')
            self.novel_intro = Book_Data.get('book_desc')
            self.authorName = Book_Data.get('book_author')
            self.chapter_list = Book_Data.get('chapter_list')
            self.lastUpdateTime = Book_Data.get('update_time')
            self.book_type = Book_Data.get('book_type')
            self.isFinish = Book_Data.get('book_status')
            self.BOOK_INFO_LIST.append(Book_Data)
            return True
        else:
            return False

    def book_show(self):
        if self.get_book_info():
            print("\n\n书名:{}\n序号:{}\n作者:{}\n分类:{}".format(
                self.bookName, self.bookid, self.authorName, self.book_type))
            print("简介:{}\n更新时间:{}\n{}".format(
                self.novel_intro, self.lastUpdateTime, self.isFinish))
            """建立文件夹和文件"""
            self.os_file()
            Download().ThreadPool(self.chapters(), self.BOOK_INFO_LIST)
        else:
            print('书籍信息获取失败！')

    def chapters(self):
        chapters_list = []
        for chapter_id_num, chapter_id in enumerate(range(len(self.chapter_list))):
            """跳过已经下载的章节"""
            if self.chapter_list[chapter_id_num] in ''.join(self.config_bookname()):
                print(self.chapter_list[chapter_id_num], '已经下载过')
                continue
            url_num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
            chapters_list.append(self.chapterurl.format(url_num, self.bookid, chapter_id))
        print('开始下载 {} ,一共剩余{}章'.format(self.bookName, len(chapters_list)))
        return chapters_list
        
        # 单线程
        #     for chapter_id_num, chapter_id in enumerate(track(range(len(self.chapter_list)))):
        #         url_num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
        #         book_title = self.chapter_list[chapter_id_num]
        #         """跳过已经下载的章节"""
        #         if self.chapter_list[chapter_id_num] in ''.join(self.config_bookname()):
        #             print(self.chapter_list[chapter_id_num], '已经下载过')
        #             continue
        #         url = self.chapterurl.format(url_num, self.bookid, chapter_id)
        #         content = self.getUtil(url)['data']
        #         """跳过屏蔽章节"""
        #         if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
        #             print(book_title)
        #             content_title = "\n\n{}\n{}".format(book_title, content_(content))
        #             self.write_txt(content_title, book_title, chapter_id_num)
        #         else:
        #             print(f"{self.chapter_list[chapter_id_num]}这是屏蔽章节，跳过下载")
                    
        #     with open(os.path.join("Download", self.bookName + '.txt'), 'w', encoding='utf-8') as f:
        #         self.filedir()
        #         print(f'\n小说 {self.bookName} 下载完成')
        
        
        
    def os_file(self):
        self.main_path = os.getcwd()  # 项目路径
        # 创建Download文件夹
        if not os.path.exists(Vars.cfg.data.get('output_dir')):
           os.mkdir(Vars.cfg.data.get('output_dir'))
           print(f'已在{self.main_path}创建Download文件夹')

        # 创建config_json文件夹
        if not os.path.exists(Vars.cfg.data.get('save_dir')):
           os.mkdir(Vars.cfg.data.get('save_dir'))
           print(f'已在{self.main_path}创建config文件夹')

        if not os.path.exists(os.path.join('config', self.bookName)):
            os.makedirs(os.path.join('config', self.bookName))

        # 创建list文本
        if not (os.path.join(self.main_path, "list.txt")):
           file = open(os.path.join(self.main_path, "list.txt"),
                       'a', encoding='utf-8')

        # 创建txt文本
        if not os.path.exists(os.path.join(Vars.cfg.data.get('output_dir'), f"{self.bookName}.txt")):
            open(os.path.join(Vars.cfg.data.get('output_dir'),
                        f"{self.bookName}.txt"), "a", encoding='utf-8')