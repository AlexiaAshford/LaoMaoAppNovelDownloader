    def writeEpubPoint(self,downloaded_list):
        save_epub_path = os.path.join("epub", self.bookName, f"{self.bookName}.yaml")
        with open(save_epub_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(downloaded_list, yaml_file, allow_unicode=True)
            
            
    def readEpubPoint(self):
        downloadedList = []
        save_epub_path = os.path.join("epub", self.bookName, f"{self.bookName}.yaml")
        if os.path.exists(save_epub_path):
            with open(save_epub_path, "r", encoding="utf-8") as yaml_file:
                downloadedList = yaml.load(yaml_file.read())
        return downloadedList

    def download2epub(self, bookid):
        self.get_bookid(bookid)
        default_style = '''
            body {font-size:100%;}
            p{
                font-family: Auto;
                text-indent: 2em;
            }
            h1{
                font-style: normal;
                font-size: 20px;
                font-family: Auto;
            }      
            '''
        ic = None
        # TODO: 创建一个EPUB文件
        if not os.path.exists('./epub'):
            os.mkdir('./epub')
        if not os.path.exists('./epub/' + self.bookName):
            os.mkdir('./epub/' + self.bookName)
        downloadedList = self.readEpubPoint()
        C = [None] * len(self.chapters_id_list)
        book = epub.EpubBook()
        book.set_identifier(self.bookid)
        book.set_title(self.bookName)
        book.set_language('zh-CN')
        book.add_author(self.authorName)
        ic = epub.EpubHtml(title='简介', file_name='intro.xhtml', lang='zh-CN')
        ic.content = '<html><head></head><body><h1>简介</h1><p>' + self.novel_intro + '</p>' + '<p>系统标签：' + self.novel_tag +'</p></body></html>'
        book.add_item(ic)

        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
                                    content=default_style)
        book.add_item(default_css)
        x = 0
        for chapterid in track(self.chapters_id_list):
            """断点下载，跳过已经存在本地的章节id"""
            if chapterid in downloadedList:
                continue
            chapters = self.get_requests(f'http://api.aixdzs.com/chapter/{chapterid}')
            
            c1 = ''
            chapter_title = chapters['chapter']['title']
            print("{}: {}".format(self.bookName, chapter_title))
            text = chapters['chapter']['body']  # 获取正文
            text_list = text.split('\n')
            for t in text_list:
                if chapter_title in t:  # 在正文中移除标题
                    continue
                if '[img' in t[:5]:
                    continue
                t = t.strip()
                c1 += '<p>' + t + '</p>'
            C[x] = epub.EpubHtml(title=chapter_title, file_name='chapter_' + chapterid +'.xhtml',lang = 'zh-CN',uid='chapter_' + chapterid)
            # c2 = self.download_insert_pict(book,text = text, chapterid=chapterid)
            C[x].content = '<h1>' + chapter_title + '</h1>' + c1
            C[x].add_item(default_css)
            # print("\t\t",j[-1],':已完成下载')
            downloadedList.append(chapterid)
            x += 1

        else:
            print("全本小说已经下载完成")
