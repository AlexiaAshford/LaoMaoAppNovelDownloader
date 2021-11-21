from API import HttpUtil, UrlConstants
from API.AesDecrypt import decrypt, example
from instance import *
import threading
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
        write(os.path.join(Vars.cfg.data.get('output_dir'),f'{self.bookName}.txt'), 'w')
        for filename in file_names_list: 
            config_file = open(os.path.join(meragefiledir, filename), 'r', encoding='utf-8').read()
            if Vars.cfg.data.get('shield') not in config_file:
                write(os.path.join(Vars.cfg.data.get('output_dir'),
                        f'{self.bookName}.txt'), 'a', config_file)
            else:
                continue

    def ThreadPool(self, chapters_url_list, info_dict):
        self.bookid = info_dict.get('book_id')
        self.bookName = info_dict.get('book_title')
        self.novel_intro = info_dict.get('book_desc')
        self.authorName = info_dict.get('book_author')
        self.chapter_list = info_dict.get('chapter_list')
        self.lastUpdateTime = info_dict.get('update_time')
        self.book_type = info_dict.get('book_type')
        self.isFinish = info_dict.get('book_status')
        """多线程并发实现"""

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
            nonlocal lock_tasks_list, lock_progress, tasks  # progress, prgtask
            
            while tasks:
                lock_tasks_list.acquire()
                url, number = tasks.pop()
                lock_tasks_list.release()
                self.progress_num += 1
                print(
                    f'下载进度:{self.progress_num}/{len(self.chapters_url_list)}', end="\r")

                book_title = del_title(self.chapter_list[number-1])
                # print(book_title)
                fd = write(
                    os.path.join(self.save_dir, self.bookName,f"{number}.{book_title}.txt"),
                    'w',
                )
                content = content_(HttpUtil.get(url).get('data'))
                # print(content)
                fd.write('\n\n\n{}\n{}'.format(book_title, content))

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
