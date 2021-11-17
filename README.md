# LaoMaoAppNovelDownloader
## 老猫小说APP爬虫

---
## 实现功能
<ul>
<li>支持多线程，默认为6线程</li>
<li>通过Bookid下载小说</li>
<li>通过书名下载小说</li>
<li>通过分类序号批量下载小说</li>
</ul>

### 环境需求

<ul>

<li>Python3.4或以上</li>

</ul>
### 使用方法
<li>本项目是基于fire模块实现的纯命令行项目</li>
<li>你可以输入python run.py help获取详细</li>
<li>
help                                                --- 显示使用说明
quit                                                --- 退出正在运作的程序
d + bookid                                          --- 下载指定小说章节文本
name + bookname                                     --- 输入书名下载小说文本
tag + tagname                                       --- 下载全站标签书籍信息
</li>

### 依赖包

<ul>


<li>request</li>

<li>os</li>

<li>EbookLib</li>
  
<li>time</li>

<li>sys</li>

<li>rich</li>

  
</ul>

### 安装依赖包

`pip install -r requirement.txt`

