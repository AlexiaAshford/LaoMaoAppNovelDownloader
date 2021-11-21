from instance import *
from API import HttpUtil, UrlConstants

class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def Login_account(self):
        user_data = {'account': self.username, 'pwd': self.password}
        login_user = HttpUtil.post(UrlConstants.USER_LOGIN, data=user_data)
        # print(login_user)
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
            print(login_msg, '自动注册')
            self.register()



    def register(self):
        user_data = {'account': self.username, 'pwd': self.password}
        register_info = HttpUtil.post(UrlConstants.USER_REGISTER, data=user_data)
        register_msg, register_code, register_data = (
        register_info.get('msg'), register_info.get('code'), register_info.get('data'))
        
        if register_msg == '该账号已存在！' or register_code == 0:
            print(register_msg, ',不在进行注册，请检查账号或密码是否正确')
            
        elif register_data != []:
            user_id, nickname, user_token = (
                register_data['user_id'], str(register_data['nickname']),
                register_data['user_token']
            )
            Vars.cfg.data['nickname'] = nickname
            Vars.cfg.data['user_token'] = user_token
            Vars.cfg.data['user_id'] = user_id
            Vars.cfg.data['password'] = self.password
            Vars.cfg.save()
            print("{} login successfully!".format(nickname))