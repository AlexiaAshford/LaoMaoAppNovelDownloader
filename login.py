from instance import *
from .HttpUtil import Util


class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = 'https://api.laomaoxs.com/user/login'


    def Login_account(self):
        data = {'account': self.username, 'pwd': self.password}
        login_user = Util.post(self.login_url, data)
        login_info, login_code, login_msg = (
            login_user.get('data'), login_user.get('code'),
            login_user.get('msg'))
        if login_code == 1 and login_msg == 'ok':
            user_id, nickname, user_account, user_sex, user_token, user_img = (
                login_info['user_id'], str(login_info['nickname']),
                login_info['user_account'], login_info['user_sex'],
                login_info['user_token'], login_info['user_img'])
            Vars.cfg.data['nickname'] = nickname
            Vars.cfg.data['user_token'] = user_token
            Vars.cfg.data['user_id'] = user_id
            Vars.cfg.save()
            print("{} login successfully!".format(nickname))

        elif login_code == 0 and login_msg == '账号或密码错误！':
            print(login_msg)
