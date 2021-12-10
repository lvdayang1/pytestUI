from pages.login_page import LoginPage
import pytest


class TestUserLoginPage():

    @pytest.fixture(autouse=True)
    def open_register(self, loginPage:LoginPage):
        loginPage.open("https://test.innocity.com")

    def test_login_1(self, loginPage:LoginPage):
        ''''''
        loginPage.click_login_link()
        loginPage.input_username("745292340@qq.com")
        loginPage.input_password("111111")
        LoginPage.click_login_btn()
        # 断言
        assert loginPage.lonin_success() == "消息中心"

if __name__ == "__main__":
    pytest.main()