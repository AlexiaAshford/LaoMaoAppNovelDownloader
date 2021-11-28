import requests
from lxml import etree
import urllib
import re
import os
import zipfile
import shutil

class Epub:
    
    def __init__(self):
        self.book_name = None
        self.chapter_title = None
        self.intro = None
        self.authorName = None
        self.content = None
    def create_mimetype(self):
        with open(self.book_name + '/' + 'mimetype') as f:
            f.write('application/epub+zip')

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
        self.file_chapter_name = str(self.number).rjust(4, "0") + '-' + f'{self.chapter_title}'
        path = os.path.join(self.book_name, 'OEBPS', 'Text', self.file_chapter_name + '.xhtml')
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(chaptrt_content)
            
            
    def style_flie(args):
        
        """book_name/OEBPS/style/nav.css"""
        nav_css = ''
        nav_css += 'body {font-family: Auto;}\r\n'
        nav_css += 'p{font-family: Auto;\r\ntext-indent: 2em;}\r\n'
        nav_css += 'h2 {text-align: left;\r\ntext-transform: uppercase;\r\nfont-weight: 200;}\r\n'
        nav_css += 'ol {list-style-type: none;}\r\n'
        nav_css += 'ol > li:first-child {margin-top: 0.3em;}\r\n'
        nav_css += "nav[epub|type~='toc'] > ol > li > ol  {list-style-type:square;}\r\n"
        nav_css += "nav[epub|type~='toc'] > ol > li > ol > li {margin-top: 0.3em;}\r\n"
        
        
        """book_name/OEBPS/style/default.css"""
        default_css = ''
        default_css += "body {font-size:100%;}\r\n"
        default_css += "p{font-family: Auto;\r\ntext-indent: 2em;}\r\n"
        default_css += "h1{font-style: normal;\r\nfont-size: 20px;\r\nfont-family: Auto;}\r\n"
            
            
    def create_info(self,epub,path,index,rollSign):
        intro_cover = ''
        intro_cover += "<?xml version='1.0' encoding='utf-8'?>\r\n<!DOCTYPE html>"
        intro_cover += '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="zh-CN" xml:lang="zh-CN">'
        intro_cover += '<head>\r\n<title>书籍封面</title>\r\n</head>'
        """图片路径../Images/cover.png"""
        intro_cover += '<body>\r\n<div style="text-align: center; padding: 0pt; margin: 0pt;">\r\n'
        intro_cover += '<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 179 248" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">'
        intro_cover += '<image height="248" width="179" xlink:href="../Images/cover.jpg"></image>\r\n</svg>\r\n'
        intro_cover += '</div>\r\n</body>\r\n</html>'
        text = f'<h1>书名:{self.bookName}</h1>\r\n' + \
            f'<h3>序号:{self.bookid}</h3>\r\n' + \
            f'<h3>作者:{self.authorName}</h3>\r\n' + \
            f'<h3>更新:{self.lastUpdateTime}</h3>\r\n' + \
            f'<h3>标签:{self.tag}</h3>\r\n' + \
            f'<h3>简介:{self.intro}</h3>'
        text = re.sub('</body>\r\n</html>', text + '\r\n</body>\r\n</html>', intro_cover)
        with open('/OEBPS/Text/cover.xhtml', 'w', encoding='utf-8') as f:
            f.write(text)



    def create_container(self):
        """bookname/META-INF/container.xml"""
        container_infp = ''
        container_infp += "<?xml version='1.0' encoding='utf-8'?>\r\n"
        container_infp += '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\r\n'
        container_infp += '<rootfiles>\r\n<rootfile media-type="application/oebps-package+xml" full-path="EPUB/content.opf"/>'
        container_infp += '</rootfiles>\r\n</container>'





def FunctionName(args):
    
    """
<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta content="707121" name="dtb:uid"/>
    <meta content="0" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>《勇者千金不想工作！！！》卷一 海港都市柯斯特篇</text>
  </docTitle>
  <navMap>
    <navPoint id="{self.file_chapter_name}">
      <navLabel>
        <text>{self.chapter_title}</text>
      </navLabel>
      <content src="{self.file_chapter_name}.xhtml"/>
    </navPoint>
  </navMap>
</ncx>
"""