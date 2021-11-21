from instance import *
from API.LaoMaoxsAPI import Download
from API import UrlConstants


class BOOK:
    bookid = None
    bookName = None
    novel_intro = None
    authorName = None
    chapter_list = None
    book_type = None
    isFinish = None

    def __init__(self, BOOK_INFO):
        self.book_info = BOOK_INFO
        self.book_info_msg = BOOK_INFO.get('msg')
        self.book_info_code = BOOK_INFO.get('code')
        self.book_info_data = self.book_info.get('data')
        self.save_dir = Vars.cfg.data.get('save_dir')
        self.output_dir = Vars.cfg.data.get('output_dir')
    def config_bookname(self):
        return os.listdir(os.path.join('config', self.bookName))

    def get_book_info(self):
        if self.book_info_msg == 'ok':
            self.bookid = self.book_info_data.get('book_id')
            self.bookName = self.book_info_data.get('book_title')
            self.novel_intro = self.book_info_data.get('book_desc')
            self.authorName = self.book_info_data.get('book_author')
            self.chapter_list = self.book_info_data.get('chapter_list')
            self.lastUpdateTime = time.localtime(
                self.book_info_data.get('update_time'))
            self.lastUpdateTime = time.strftime(
                "%Y-%m-%d %H:%M:%S", self.lastUpdateTime)
            self.book_type = self.book_info_data.get('book_type')
            self.isFinish = self.book_info_data.get('book_status')
            return True
        else:
            return False

    def book_show(self):
        if self.get_book_info():
            self.os_file()
            show_intro = "书名:{}\n序号:{}\n作者:{}\n分类:{}\n更新:{}".format(
                self.bookName, self.bookid, self.authorName,
                self.book_type, self.lastUpdateTime)
            print(show_intro)
            show_intro += "\n简介信息:{}\n".format(content_(self.novel_intro))

            save_dir_bookflie = os.path.join(
                Vars.cfg.data.get('save_dir'), self.bookName)
            if not os.path.exists(save_dir_bookflie):
                os.makedirs(save_dir_bookflie)

            write(os.path.join(save_dir_bookflie, '0.intro.txt'), 'w', show_intro)

            """建立文件夹和文件"""

            Download().ThreadPool(self.chapters(), self.book_info_data)
        else:
            self.book_info_msg

    def chapters(self):
        chapters_list = []
        config_bookname = self.config_bookname()
        for chapter_id_num, chapter_id in enumerate(range(len(self.chapter_list))):
            """跳过已经下载的章节"""
            chapter_title = self.chapter_list[chapter_id_num]
            if del_title(chapter_title) in ''.join(config_bookname):
                # if self.chapter_list[chapter_id_num] in ''.join(self.config_bookname()):
                # print(self.chapter_list[chapter_id_num], '已经下载过')
                continue
            url_num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
            chapters_list.append(UrlConstants.CHAP_CONTENT.format(
                url_num, self.bookid, chapter_id))
        if len(chapters_list) == 0:
            print("没有需要下载的章节")
        else:
            print('开始下载 {} ,一共剩余{}章'.format(self.bookName, len(chapters_list)))
        return chapters_list

    def os_file(self):
        self.main_path = os.getcwd()  # 项目路径
        # 创建Download文件夹
        if not os.path.exists(self.output_dir):
           os.mkdir(self.output_dir)
           print(f'已在{self.main_path}创建{self.output_dir}文件夹')

        # 创建config文件夹
        if not os.path.exists(self.save_dir):
           os.mkdir(self.save_dir)
           print(f'已在{self.main_path}创建{self.save_dir}文件夹')

        if not os.path.exists(os.path.join(self.save_dir, self.bookName)):
            os.makedirs(os.path.join(self.save_dir, self.bookName))

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
