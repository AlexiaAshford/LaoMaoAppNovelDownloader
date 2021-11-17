# LaoMaoAppNovelDownloader
## 老猫小说APP爬虫 
### 关于仓库
<li>这是重构的老猫小说项目，可以理解成2.0版本</li>
<li>重构前的项目名字为：Laomao_Novel_Download ，Laomao_Novel_Download这个项目也是我写的，不过现在已经删除</li>

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
```  
help                                                --- 显示使用说明
quit                                                --- 退出正在运作的程序
name + bookname                                     --- 输入书名下载小说文本
tag + tagname                                       --- 下载全站标签书籍信息
d + bookid                                          --- 下载指定小说章节文本
```  

### 依赖包

<ul>


<li>request</li>

<li>os</li>

<li>fire</li>
  
<li>time</li>

<li>sys</li>

<li>rich</li>

  
</ul>

### 安装依赖包

`pip install -r requirement.txt`

