from common.base import Base


class LoginPage(Base):

    '''登录链接'''
    login_loc = ("link text", u"登录")
    '''账号'''
    username_loc = ("id", "userName")
    '''密码'''
    password_loc = ("id", "password")
    '''登录按钮'''
    btn_loc = ("id", "login")
    '''登录成功'''
    success_loc = ("classname", "xl_btn")

    def click_login_link(self):
        '''点击登录链接'''
        self.click(self.login_loc)

    def input_username(self, text):
        self.click(self.username_loc)
        self.clear(self.username_loc)
        '''输入账号'''
        self.send(self.username_loc, text)

    def input_password(self, text):
        self.click(self.password_loc)
        self.clear(self.password_loc)
        '''输入密码'''
        self.send(self.password_loc, text)

    def click_login_btn(self):
        '''点击提交按钮'''
        self.click(self.btn_loc)

    def lonin_success(self):
        '''存在消息中心，登录成功'''
        return self.get_text(self.success_loc)




