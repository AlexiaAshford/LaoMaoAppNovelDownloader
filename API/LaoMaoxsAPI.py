from API import HttpUtil, UrlConstants
from API.AesDecrypt import decrypt, example
from instance import *
import requests, threading
# from rich.progress import DownloadColumn, TextColumn, Progress, BarColumn, TimeRemainingColumn


class Download:
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.progress_num = 0
        self.save_dir = Vars.cfg.data.get('save_dir')
        self.output_dir = Vars.cfg.data.get('output_dir')
        self.max_worker = Vars.cfg.data.get('max_workers_number')

    def filedir(self):
        meragefiledir = os.path.join(self.save_dir, self.bookName)
        file_names_list = os.listdir(meragefiledir)
        file_names_list.sort(key=lambda x: int(x.split('.')[0]))
        for filename in file_names_list:  # 先遍历文件名
            #遍历单个文件，读取行数
            for line in open(os.path.join(meragefiledir, filename), encoding='utf-8'):
                if Vars.cfg.data.get('shield') in line or \
                    Vars.cfg.data.get('shield2') in line:
                    continue
                else:
                    write(os.path.join(Vars.cfg.data.get('output_dir'), f'{self.bookName}.txt'), 'a', line)

    def SearchBook(self, bookname):
        urls = ['https://api.laomaoxs.com/Search/index?key={}&page={}'.format(
            bookname, i) for i in range(100)]
            
        # print(url)
        for url in urls:
            if not HttpUtil.get(url)['data']:
                break
            """存储bookid进列表中"""
            search_book = [data['book_id']
                           for data in HttpUtil.get(url)['data']]
        return search_book

    def class_list(self, Tag_Number):
        class_list_bookid = []
        for i in range(10000):
            url = f'https://api.laomaoxs.com/novel/lists?order=0&status=0&sex=1&page={i}&type={Tag_Number}'
            if not HttpUtil.get(url)['data']:
                print('排行榜已经下载完毕')
                break
            for data in HttpUtil.get(url)['data']:
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
            if not HttpUtil.get(url)['data']:
                print('分类已经下载完毕')
                break
            for data in HttpUtil.get(url)['data']:
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
        # print('多进程', self.Read.get('Multithreading'))
        # executor = ThreadPoolExecutor(max_workers=self.max_worker)
        # task_list = []
        # for number, book_url in enumerate(chapters_url_list):
        #     task = partial(self.ThreadPool_download, book_url, number)
        #     task_list.append(executor.submit(task))
            
        # if task_list:
        #     for chapter_num in range(len(task_list)):
        #         time.sleep(0.1)
        #         print(chapter_num +1, '/', len(task_list), end = "\r")
            
        #     self.filedir()
        #     print(f'\n小说 {self.bookName} 下载完成')
        # else:
        #     self.filedir()

        # 创建 rich 进度条
        lock_tasks_list = threading.Lock()
        lock_progress = threading.Lock()
        tasks = []
        threads = []
        # progress = Progress(
        #     # TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        #     BarColumn(bar_width=None),
        #     "[progress.percentage]{task.percentage:>3.1f}%",
        #     "•",
        #     DownloadColumn(),
        #     # "•",
        #     # TransferSpeedColumn(),
        #     "•",
        #     TimeRemainingColumn(),
        # )

        # 生成下载队列.
        for number, book_url in enumerate(chapters_url_list):
            tasks.append(
                (UrlConstants.WEB_SITE + book_url, number)
            )
            
        # prgtask = progress.add_task(
        #     "Download", total=len(tasks)
        #     )
        self.chapters_url_list = chapters_url_list
        # print(self.chapters_url_list)
        def downloader():
            """多线程下载函数"""
            nonlocal lock_tasks_list, lock_progress, tasks # progress, prgtask

            session = requests.Session()
            
            while tasks:
                lock_tasks_list.acquire()
                url, number = tasks.pop()
                lock_tasks_list.release()
                self.progress_num += 1
                print(f'下载进度:{self.progress_num}/{len(self.chapters_url_list)}', end = "\r")
                
                book_title = del_title(self.chapter_list[number-1])
                # print(book_title)
                fd = write(
                    os.path.join(self.save_dir, self.bookName, f"{number}.{book_title}.txt"),
                    'w',
                )
                with session.get(url, headers=HttpUtil.headers) as response:
                    content = example(decrypt(response.content)).get('data')
                    fd.write('\n\n\n{}\n{}'.format(book_title, content_(content)))

                    lock_progress.acquire()
                    # progress.update(prgtask, advance=1)
                    lock_progress.release()
                
            
        for _ in range(self.max_worker):
            th = threading.Thread(target=downloader)
            threads.append(th)
            th.start()

        # wait downloader
        for th in threads:
            th.join()

        self.filedir()
        print(f'\n小说 {self.bookName} 下载完成\n\n')


