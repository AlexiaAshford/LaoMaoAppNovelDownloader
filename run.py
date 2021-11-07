import click
from API import Settings
from API import LaoMaoxsAPI

Settings.Set().NewSettings()

@click.command()
def shell_book(bookid, pool):
    Download.GetBook(bookid)
    if pool:
        Download.ThreadPool(Read['max_workers_number'])
    else:
        Download.chapters(pool=False)


@click.command()
def shell_login(login):
    usernames = login.split(',')[0]
    passwords = login.split(',')[1]
    Download.Login(usernames, passwords)


@click.command()
def shell_maxn_umber(max):
    if max.isdigit():
        Read['max_workers_number'] = 12 if int(max) > 12 else int(max)
        print("线程已经设置为", Read['max_workers_number'])
        Settings.Set().WriteSettings(Read)
    else:
        print(max, "不是数字，请重新输入")


def shell_book_name(name, pool):
    search_book = Download.SearchBook(name)
    for i in search_book:
        Download.GetBook(i)
        if pool:
            print("开启多线程")
            Download.ThreadPool(Read['max_workers_number'])
        else:
            Download.chapters(pool=False)


@click.command()
def shell_tag(tag, pool):
    for i in Download.class_list(tag):
        Download.GetBook(i)
        if pool:
            Download.ThreadPool(Read['max_workers_number'])
        else:
            Download.chapters(pool=False)


def shell_rank(pool):
    for i in Download.ranking():
        Download.GetBook(i)
        if pool:
            Download.ThreadPool(Read['max_workers_number'])
        else:
            Download.chapters(pool=False)


@click.command()
@click.option("--choice", prompt="please input choice", help="功能选择")
@click.option('--tag',  help="tag number")
@click.option('--bookid', help="bookid")
@click.option('--name', help="nmae")
@click.option('--login', help="账号,密码，注意需要用,隔开")
@click.option('--max', default='10', help="Set thread  pool")
@click.option('--pool', default=True, help="pool")

def shell(choice, tag, bookid, login, max, name, pool):
    if choice == 'h' or choice == 'help':
        print(Read['help'])

    if choice == 'l' or choice == 'login':
        shell_login(login)

    elif choice == 'n' or choice == 'name':
        shell_book_name(name, pool)

    elif choice == 'd' or choice == 'download':
        shell_book(bookid, pool)

    elif choice == 't' or choice == 'tag':
        shell_tag(tag, pool)

    elif choice == 'm' or choice == 'max':
        shell_maxn_umber(max)

    elif choice == 'r' or choice == 'rank':
        shell_rank()
    else:
        print("选项为不存在,请输入-h获取帮助")


if __name__ == '__main__':
    Download = LaoMaoxsAPI.Download()
    Read = Settings.Set().ReadSettings()
    shell()
