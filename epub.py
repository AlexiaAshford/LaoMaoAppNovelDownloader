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
        nav_css = ''
        nav_css += 'body {font-family: Auto;}\r\n'
        nav_css += 'p{font-family: Auto;\r\ntext-indent: 2em;}\r\n'
        nav_css += 'h2 {text-align: left;\r\ntext-transform: uppercase;\r\nfont-weight: 200;}\r\n'
        nav_css += 'ol {list-style-type: none;}\r\n'
        nav_css += 'ol > li:first-child {margin-top: 0.3em;}\r\n'
        nav_css += "nav[epub|type~='toc'] > ol > li > ol  {list-style-type:square;}\r\n"
        nav_css += "nav[epub|type~='toc'] > ol > li > ol > li {margin-top: 0.3em;}\r\n"
        
        default_css = ''
        default_css += "body {font-size:100%;}\r\n"
        default_css += "p{font-family: Auto;\r\ntext-indent: 2em;}\r\n"
        default_css += "h1{font-style: normal;\r\nfont-size: 20px;\r\nfont-family: Auto;}\r\n"
            
            
    def create_content(self):
            content_info = '''<?xml version="1.0" encoding="utf-8"?>
    <package version="3.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'''
            if self.chapter_title != '':
                content_info += "<dc:title>" + self.chapter_title + "</dc:title>"
            if self.author != '':
                content_info += "<dc:creator>" + self.authorName + "</dc:creator>"
            if self.intro != '':
                content_info += "<dc:description>" + self.intro + "</dc:description>"
            content_info += '''<meta name="cover" content="p.jpg" />
    </metadata><manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="sgc-nav.css" href="sgc-nav.css" media-type="text/css"/>
    <item id="nav.xhtml" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="p.jpg" href="p.jpg" media-type="image/jpeg" properties="cover-image"/>
    %(manifest)s
    </manifest><spine toc="ncx">
    <itemref idref="C.xhtml" />
    <itemref idref="info.xhtml" />
    <itemref idref="nav.xhtml" />
    %(spine)s
    </spine></package>'''
            manifest = ''
            spine = ''
            for html in os.listdir(path):
                basename = os.path.basename(html)
                if basename.endswith('html'):
                    manifest += '<item id="%s" href="Fonts/%s" media-type="application/xhtml+xml"/>' % (basename, basename)
                    if basename != 'C.xhtml' and basename != 'info.xhtml':
                        spine += '<itemref idref="%s"/>' % (basename)
            spine+='''<guide>
        <reference type="cover" title="封面" href="C.xhtml"/>
    </guide>'''
            epub.writestr('OEBPS/content.opf',content_info % {'manifest': manifest,'spine': spine,},compress_type=zipfile.ZIP_STORED)

    def create_info(self,epub,path,index,rollSign):
        nav_info='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head><title></title>
<meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<nav epub:type="toc" id="toc"><h1>目录</h1>
    <ol>
    '''
        sig=0
        nav_info+='''<li><a href="info.xhtml">'''+self.chapter_title+'-'+self.author+'''</a>
<ol>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename!='C.xhtml' and basename!='info.xhtml':
                    iii=0
                    if sig<len(index):
                        while index[sig] in rollSign:
                            index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                            nav_info+='''</ol></li>
    <li><a href="'''+basename+'''">
    '''+index[sig]+'''</a>
    <ol>'''
                            sig+=1
                            iii=1
                        if iii==1:
                            basename+='#v'
                        index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                        nav_info+='''<li><a href="'''+basename+'''">'''+index[sig]+'''</a></li>
    '''
                        sig+=1
        nav_info+='''</ol></li></ol></nav></body></html>'''
        epub.writestr('OEBPS/nav.xhtml',nav_info,compress_type=zipfile.ZIP_STORED)
    def create_toc(self,epub,path,index,rollSign):
        tox_info='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="" />
    <meta name="dtb:depth" content="2" />
    <meta name="dtb:totalPageCount" content="0" />
    <meta name="dtb:maxPageNumber" content="0" />
</head><docTitle><text>'''+self.chapter_title+'''</text></docTitle><navMap>'''
        sig=0
        tox_info+='''<navPoint id="0" playOrder="0">
<navLabel><text>'''+self.chapter_title+'''</text></navLabel><content src="info.xhtml"/>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename!='C.xhtml' and basename!='info.xhtml':
                    iii=0
                    if sig<len(index):
                        while index[sig] in rollSign:
                            index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                            tox_info+='''</navPoint><navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
    <navLabel><text>'''+index[sig]+'''</text></navLabel><content src="'''+basename+'''"/>'''
                            sig+=1
                            iii=1
                        if iii==1:
                            basename+='#v'
                        index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                        tox_info+='''<navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
    <navLabel><text>'''+index[sig]+'''</text></navLabel><content src="'''+basename+'''"/></navPoint>'''
                        sig+=1
        tox_info+='''</navPoint></navMap></ncx>'''
        epub.writestr('OEBPS/toc.ncx',tox_info,compress_type=zipfile.ZIP_STORED)
        
    def create_stylesheet(self,epub):
        css_info = '''nav#landmarks {
    display:none;
}
nav#page-list {
    display:none;
}
ol {
    list-style-type: none;
}
h1{font-size:1.4em;text-align:center;}h2{font-size:1.24em;text-align:center;}
.title{
text-align:center;
}
# '''+self.fontcss
#         epub.writestr('OEBPS/sgc-nav.css',css_info,compress_type=zipfile.ZIP_STORED)
#     def createEpub(self,epub,xaut,xtitle,ti,index,rollSign,path):
#         self.author=xaut
#         self.chapter_title=xtitle
#         self.create_mimetype(epub)     
#         self.create_container(epub)  
#         os.chdir(ti)
#         ppp=os.getcwd()
#         self.create_content(epub,ppp)
#         self.create_info(epub,ppp,index,rollSign)
#         self.create_toc(epub,ppp,index,rollSign)
#         self.create_stylesheet(epub)
#         for html in os.listdir('.'):
#             basename = os.path.basename(html)
#             if basename.endswith('jpg'):
#                 epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
#             if basename.endswith('html'):
#                 epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
#         epub.close()
#         os.chdir(path)
#         shutil.rmtree(ppp)