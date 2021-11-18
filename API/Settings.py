from instance import *


def setup_config():
    Vars.cfg.load()
    config_change = False
    if type(Vars.cfg.data.get('help')) is not str or Vars.cfg.data.get('help') == "":
        Vars.cfg.data['help'] = "输入 - 加上首字母\nh | help\t\t\t\t\t\t--- 显示说明\nq | quit\t\t\t\t\t\t--- 退出正在运作的程序\nc | cookie\t\t\t\t\t\t--- 检测本地的cookie凭证\nb | b + bookid\t\t\t\t\t\t--- 下载指定小说章节文本\nu | u + url\t\t\t\t\t\t--- 下载指定小说章节文本\nn | n + bookname\t\t\t\t\t--- 输入书名下载小说文本\nt | t + tagname\t\t\t\t\t\t--- 下载全站标签书籍信息"
        config_change = True

    if type(Vars.cfg.data.get('key')) is not str or Vars.cfg.data.get('key') == "":
        Vars.cfg.data['key'] = "b23c159r9t88hl2q"
        config_change = True

    # if type(Vars.cfg.data.get('iv')) is not str or Vars.cfg.data.get('iv') == "":
    #     Vars.cfg.data['iv'] = b'8yeywyJ45esysW8M'
    #     config_change = True

    if type(Vars.cfg.data.get('output_dir')) is not str or Vars.cfg.data.get('output_dir') == "":
        Vars.cfg.data['output_dir'] = "Download"
        config_change = True
    if type(Vars.cfg.data.get('save_dir')) is not str or Vars.cfg.data.get('save_dir') == "":
        Vars.cfg.data['save_dir'] = "Config"
        config_change = True

    if type(Vars.cfg.data.get('Open_ThreadPool')) is not bool:
        Vars.cfg.data['Open_ThreadPool'] = True
        config_change = True

    if type(Vars.cfg.data.get('tocken')) is not str or Vars.cfg.data.get('tocken') == "":
        Vars.cfg.data['tocken'] = ""
        config_change = True
    if type(Vars.cfg.data.get('shield2')) is not str or Vars.cfg.data.get('shield2') == "":
        Vars.cfg.data['shield2'] = "　　编辑正在手打中，稍后点击右上角刷新当前章节！"
        config_change = True
    if type(Vars.cfg.data.get('shield')) is not str or Vars.cfg.data.get('shield') == "":
        Vars.cfg.data['shield'] = "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！"
        config_change = True
    if type(Vars.cfg.data.get('max_workers_number')) is not int:
        Vars.cfg.data['max_workers_number'] = 16
        config_change = True

    if config_change:
        Vars.cfg.save()
