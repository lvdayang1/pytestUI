import pytest
from pages.login_page import LoginPage


class TestUserLoginPage():

    @pytest.fixture(autouse=True)
    def open_register(self, usersLoginPage:LoginPage):
        usersLoginPage.open("")

    def login(self, usersLoginPage:LoginPage):
        ''''''
        usersLoginPage.click_login_link()
        usersLoginPage.input_username("745292340@qq.com")
        usersLoginPage.input_password("111111")
        usersLoginPage.click_login_btn()
        # 断言
        assert usersLoginPage.lonin_success() == "消息中心"