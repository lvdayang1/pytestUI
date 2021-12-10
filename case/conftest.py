import pytest
from selenium import webdriver
from common.oracle import MyDB
from pages.login_page import LoginPage


@pytest.fixture(scope="session", name="driver")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # quit是退出浏览器
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    url = "https://test.innocity.com"
    return url

@pytest.fixture(scope="session")
def db():
    _db = MyDB()
    _db.connectDB()
    yield _db
    _db.closeDB()

@pytest.fixture(scope="session")
def loginPage(driver, base_url):
    login = LoginPage(driver, base_url)
    return login
