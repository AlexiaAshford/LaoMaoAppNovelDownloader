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
        

    def get_book_info(self):
        if self.book_info_msg == 'ok':
            self.bookid = self.book_info_data.get('book_id')
            self.bookName = self.book_info_data.get('book_title')
            self.book_type = self.book_info_data.get('book_type')
            self.isFinish = self.book_info_data.get('book_status')
            self.novel_intro = self.book_info_data.get('book_desc')
            self.authorName = self.book_info_data.get('book_author')
            self.chapter_list = self.book_info_data.get('chapter_list')
            self.lastUpdateTime = time_(self.book_info_data.get('update_time'))
            return 200
        else:
            return 404

    def book_show(self):
        if self.get_book_info() == 200:
            """创建配置 output_dir 和 创建config 文件夹 """ 
            mkdir(self.output_dir); mkdir(self.save_dir)
            """创建config/bookname/ 文件夹 """
            makedirs(self.save_dir, self.bookName)
            """打印书名信息"""
            show_intro = "书名:{}\n序号:{}\n作者:{}\n分类:{}\n更新:{}".format(
                self.bookName, self.bookid, self.authorName,
                self.book_type, self.lastUpdateTime)
            print(show_intro)
            
            show_intro += "\n简介信息:{}\n".format(content_(self.novel_intro))
            """保存书籍详细到 config/bookname/0.intro.txt"""
            write(os.path.join(self.save_dir, self.bookName, '0.intro.txt'), 'w', show_intro)

            """执行下载任务！"""
            chapter_list = self.chapters()
            if chapter_list == 'null':
                print("没有需要下载的章节\n\n")
            else:
                print(f'开始下载 {self.bookName} ,剩余{len(chapter_list)}章')
                Download().ThreadPool(self.chapters(), self.book_info_data)
        elif self.get_book_info() == 404:
            print(self.book_info_msg)

    def chapters(self):
        chapter_list = list()
        config_bookname = os.listdir(os.path.join(self.save_dir, self.bookName))
        for chapter_id_num, chapter_id in enumerate(range(len(self.chapter_list))):
            """跳过已经下载的章节"""
            chapter_title = self.chapter_list[chapter_id_num]
            if del_title(chapter_title) in ''.join(config_bookname):
                continue
            url_num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
            
            chapter_url = UrlConstants.CONTENT.format(url_num, self.bookid, chapter_id)
            chapter_list.append(chapter_url)
        
        if len(chapter_list) == 0:
            return 'null'
        return chapter_list

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
