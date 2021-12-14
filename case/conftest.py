import time
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

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    # print(terminalreporter.stats)
    total = terminalreporter._numcollected
    passed= len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed=len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error=len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped=len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    successful = len(terminalreporter.stats.get('passed', []))/terminalreporter._numcollected*100
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times: %.2f' % duration, 'seconds')

    with open("./result/result.txt", "w") as fp:
        fp.write("创新城UI自动化测试结果：\n")
        fp.write("TOTAL=%s" % total+"\n")
        fp.write("PASSED=%s" % passed+"\n")
        fp.write("FAILED=%s" % failed+"\n")
        fp.write("ERROR=%s" % error+"\n")
        fp.write("SKIPPED=%s" % skipped+"\n")
        fp.write("SUCCESSFUL=%.2f%%" % successful+"\n")
        fp.write("TOTAL_TIMES=%.2fs" % duration)