import requests
from instance import *
import urllib
import re
import os
import zipfile
import shutil


Vars.cfg.load()


class Epub:

    def __init__(self, book_name, book_id, author_name, tag_name, book_description, lastUpdateTime):
        self.book_name = book_name
        self.bookid = book_id
        self.book_description = book_description
        self.author_name = author_name
        self.tag_name = tag_name
        self.lastUpdateTime = lastUpdateTime

    def create_mimetype(self):
        write(os.path.join(Vars.cfg.data.get('save_dir'),
              self.book_name, 'mimetype'), 'w', 'application/epub+zip')

    def set_cover(self, url: str, png_name=None):
        if png_name is None:
            image_path = self.tempdir + '/OEBPS/Images/cover.jpg'
        else:
            image_path = self.tempdir + '/OEBPS/Images/' + png_name
        if os.path.exists(image_path):
            if os.path.getsize(image_path) != 0:
                return
        for retry in range(10):
            try:
                urllib.request.urlretrieve(url, image_path)
                return
            except OSError as e:
                print('下载封面图片失败')

    def create_content(self):
        chaptrt_content = ''
        chaptrt_content += "<?xml version='1.0' encoding='utf-8'?>\r\n"
        chaptrt_content += '<!DOCTYPE html>\r\n'
        chaptrt_content += '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="zh-CN" xml:lang="zh-CN">\r\n'
        chaptrt_content += '<head>\r\n<title>{self.chapter_title}</title>\r\n'
        chaptrt_content += '<link href="style/default.css" rel="stylesheet" type="text/css"/>\r\n</head>\r\n'
        chaptrt_content += f"<body>\r\n<h1>{self.chapter_title}</h1>\r\n<p></p>\r\n"
        content_line = self.content.split('\n')
        for line in content_line:
            chaptrt_content += f"<p>{line}</p>\r\n"
        chaptrt_content += "\r\n</body>\r\n</html>"
        self.file_chapter_name = str(self.number).rjust(
            4, "0") + '-' + f'{self.chapter_title}'
        path = os.path.join(self.book_name, 'OEBPS', 'Text',
                            self.file_chapter_name + '.xhtml')

        with open(path, 'w', encoding='utf-8') as file:
            file.write(chaptrt_content)

    def style_flie(self):
        style_flie_path = os.path.join(Vars.cfg.data.get(
            'save_dir'), self.book_name, 'OEBPS', 'style')
        if not os.path.exists(style_flie_path):
            os.mkdir(style_flie_path)
        """book_name/OEBPS/style/nav.css"""
        nav_css = ''
        nav_css += 'body {font-family: Auto;}\r\n'
        nav_css += 'p{font-family: Auto;\r\ntext-indent: 2em;}\r\n'
        nav_css += 'h2 {text-align: left;\r\ntext-transform: uppercase;\r\nfont-weight: 200;}\r\n'
        nav_css += 'ol {list-style-type: none;}\r\n'
        nav_css += 'ol > li:first-child {margin-top: 0.3em;}\r\n'
        nav_css += "nav[epub|type~='toc'] > ol > li > ol  {list-style-type:square;}\r\n"
        nav_css += "nav[epub|type~='toc'] > ol > li > ol > li {margin-top: 0.3em;}\r\n"
        write(os.path.join(style_flie_path, 'nav.css'), 'w', nav_css)

        """book_name/OEBPS/style/default.css"""
        default_css = ''
        default_css += "body {font-size:100%;}\r\n"
        default_css += "p{font-family: Auto;\r\ntext-indent: 2em;}\r\n"
        default_css += "h1{font-style: normal;\r\nfont-size: 20px;\r\nfont-family: Auto;}\r\n"
        write(os.path.join(style_flie_path, 'default.css'), 'w', default_css)

    def create_info(self):
        path_cover = os.path.join(Vars.cfg.data.get(
            'save_dir'), self.book_name, "OEBPS", "Text")
        if not os.path.exists(path_cover):
            os.makedirs(path_cover)
        intro_cover = ''
        intro_cover += "<?xml version='1.0' encoding='utf-8'?>\r\n<!DOCTYPE html>"
        intro_cover += '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="zh-CN" xml:lang="zh-CN">'
        intro_cover += '<head>\r\n<title>书籍封面</title>\r\n</head>'
        """图片路径../Images/cover.png"""
        intro_cover += '<body>\r\n<div style="text-align: center; padding: 0pt; margin: 0pt;">\r\n'
        intro_cover += '<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 179 248" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">'
        intro_cover += '<image height="248" width="179" xlink:href="../Images/cover.jpg"></image>\r\n</svg>\r\n'
        intro_cover += '</div>\r\n</body>\r\n</html>'
        text = f'<h1>书名:{self.book_name}</h1>\r\n' + \
            f'<h3>序号:{self.bookid}</h3>\r\n' + \
            f'<h3>作者:{self.author_name}</h3>\r\n' + \
            f'<h3>更新:{self.lastUpdateTime}</h3>\r\n' + \
            f'<h3>标签:{self.tag_name}</h3>\r\n' + \
            f'<h3>简介:{self.book_description}</h3>'
        text = re.sub('</body>\r\n</html>', text +
                      '\r\n</body>\r\n</html>', intro_cover)
        write(os.path.join(path_cover, 'cover.xhtml'), 'w', text)

    def create_container(self):
        """bookname/META-INF/container.xml"""
        container_infp = ''
        container_infp += "<?xml version='1.0' encoding='utf-8'?>\r\n"
        container_infp += '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\r\n'
        container_infp += '<rootfiles>\r\n<rootfile media-type="application/oebps-package+xml" full-path="OEBPS/content.opf"/>'
        container_infp += '</rootfiles>\r\n</container>'
        container_flie_path = os.path.join(
            Vars.cfg.data.get('save_dir'), self.book_name, 'META-INF')
        if not os.path.exists(container_flie_path):
            os.mkdir(container_flie_path)
            write(os.path.join(container_flie_path,
                  'container.xml'), 'w', container_infp)

    def create_toc(self):
        nav = ""
        nav += "<?xml version='1.0' encoding='utf-8'?>\r\n"
        nav += '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\r\n'
        nav += '<head>\r\n<meta content="{self.bookid}" name="dtb:uid"/>\r\n'
        nav += '<meta content="0" name="dtb:depth"/>\r\n'
        nav += '<meta content="0" name="dtb:totalPageCount"/>\r\n'
        nav += '<meta content="0" name="dtb:maxPageNumber"/>\r\n'
        nav += '</head>\r\n<docTitle>\r\n'
        nav += '<text>{self.book_name}</text>\r\n'
        nav += '</docTitle>\r\n<navMap>\r\n'
        chapter_nav = ''
        chapter_nav += '<navPoint id="${chapter_title}">\r\n<navLabel>\r\n'
        chapter_nav += '<text>${chapter_title}</text>\r\n</navLabel>\r\n'
        chapter_nav += '<content src="${file_chapter_name}.xhtml"/>\r\n</navPoint>\r\n'
        nav += chapter_nav + '</navMap>\r\n</ncx>'
        toc_file_path = os.path.join(Vars.cfg.data.get(
            'save_dir'), self.book_name, "OEBPS")
        if not os.path.exists(os.path.join(toc_file_path, 'toc.ncxl')):
            write(os.path.join(toc_file_path, 'toc.ncxl'), 'a', nav)

    def add_toc(self, Volume, title, file_chapter_name):
        toc_file_path = os.path.join(Vars.cfg.data.get(
            'save_dir'), self.book_name, "OEBPS", 'toc.ncxl')
        toc_file = write(os.path.join(toc_file_path), 'r').read()
        # print(toc_file)
        add_toc = toc_file.replace('${Volume_name}', Volume)
        add_toc = add_toc.replace('${chapter_title}', title)
        add_toc = add_toc.replace('${file_chapter_name}', file_chapter_name)
        chapter_nav = '<navPoint id="${chapter_title}">\r\n<navLabel>\r\n'
        chapter_nav += '<text>${chapter_title}</text>\r\n</navLabel>\r\n'
        chapter_nav += '<content src="${file_chapter_name}.xhtml"/>\r\n</navPoint>\r\n'
        add_toc = add_toc.replace('</navMap>', chapter_nav + '\r\n</navMap>')
        write(toc_file_path, 'w', add_toc)

    def create_content_opf(self):
        content_opf = "<?xml version='1.0' encoding='utf-8'?>\r\n"
        content_opf = '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0" prefix="rendition: http://www.idpf.org/vocab/rendition/#">\r\n'
        content_opf += '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\r\n'
        content_opf += '<meta property="dcterms:modified">{self.lastUpdateTime}</meta>\r\n'
        content_opf += '<dc:identifier id="id">{self.bookid}</dc:identifier>\r\n'
        content_opf += '<dc:title>{self.book_name}</dc:title>\r\n'
        content_opf += '<dc:language>zh-CN</dc:language>\r\n'
        content_opf += '<dc:creator id="creator">{self.author_name}</dc:creator>\r\n'
        content_opf += '<meta name="generator" content="Ebook-lib 0.17.1"/>\r\n'
        content_opf += '<meta name="cover" content="cover-img"/>\r\n'
        content_opf += '</metadata>\r\n<manifest>\r\n'

        content_opf_href = '<item href="image/cover.png" id="cover-img" media-type="image/png" properties="cover-image"/>\r\n'
        content_opf_href += '<item href="Text/cover.xhtml" id="cover" media-type="application/x-dtbncx+xml"/>\r\n'
        content_opf_href += '<item href="style/default.css" id="style_default" media-type="text/css"/>\r\n'
        content_opf_href += '<item href="style/nav.css" id="style_nav" media-type="text/css"/>\r\n'
        content_opf_href += '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\r\n'
        content_opf_href += '<item href="nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>\r\n'

        content_opf_href += '<item href="Text/${file_chapter_name}.xhtml" id="${file_chapter_name}" media-type="application/xhtml+xml"/>\r\n'

        content_opf_href += '</manifest>\r\n'
        content_opf_href += '<spine toc="ncx">\r\n'
        content_opf_href += '<itemref idref="nav"/>\r\n'
        content_opf_href += '<itemref idref="$id{file_chapter_name}"/>\r\n'
        content_opf_href += '</spine>\r\n</package>\r\n'
        opf_file_path = os.path.join(Vars.cfg.data.get('save_dir'), self.book_name, "OEBPS", 'content.opf')
        if not os.path.exists(opf_file_path):
            write(opf_file_path, 'w', content_opf + content_opf_href)

    def add_content_opf(self, file_chapter_name):
        opf_file_path = os.path.join(Vars.cfg.data.get(
            'save_dir'), self.book_name, "OEBPS", 'content.opf')
        opf_file = write(os.path.join(opf_file_path), 'r').read()
        print(opf_file)
        add_opf = opf_file.replace('${file_chapter_name}', file_chapter_name)
        add_opf = add_opf.replace(
            '</manifest>', '<item href="Text/${file_chapter_name}.xhtml" id="${file_chapter_name}" media-type="application/xhtml+xml"/>\r\n</manifest>')
        add_opf = add_opf.replace('$id{file_chapter_name}', file_chapter_name)
        add_opf = add_opf.replace(
            '</spine>', '<itemref idref="$id{file_chapter_name}"/>\r\n</spine>')
        write(opf_file_path, 'w', add_opf)

    def create_nav(self):
        nav = "<?xml version='1.0' encoding='utf-8'?>"
        nav += '<!DOCTYPE html>'
        nav += '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="zh-CN" xml:lang="zh-CN">\r\n'
        nav += '<head>\r\n'
        nav += '<title>{self.book_name}</title>\r\n'
        nav += '</head>\r\n<body>\r\n'
        nav += '<nav epub:type="toc" id="id" role="doc-toc">\r\n'
        nav += '<h2>{self.book_name}</h2>\r\n'
        nav += '<ol>\r\n<li>\r\n'
        nav += '<a href="${file_chapter_name}.xhtml">${chapter_title}</a>\r\n'
        nav += '</li>\r\n</ol>\r\n</nav>\r\n</body>\r\n</html>\r\n'
        nav_file_path = os.path.join(Vars.cfg.data.get('save_dir'), self.book_name, "OEBPS", 'nav.xhtml')
        if not os.path.exists(nav_file_path):
            write(nav_file_path, 'w', nav)

if __name__ == '__main__':
    Epubs = Epub('大师姐', '43534534', '可乐', '百合', '这是一个简介', '2021年')
    Epubs.create_info()
    Epubs.style_flie()
    Epubs.create_container()
    Epubs.create_mimetype()
    Epubs.create_toc()
    Epubs.add_toc('这是卷', '这是章节', '这是路径')
    Epubs.create_nav()
    Epubs.create_content_opf()
