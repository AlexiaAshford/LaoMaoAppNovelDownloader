import requests
from lxml import etree
import sys
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
        file_chapter_name = str(self.number).rjust(4, "0") + '-' + f'{self.chapter_title}.txt'
        path = os.path.join(self.book_name, 'OEBPS', 'Text', file_chapter_name)
        
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
