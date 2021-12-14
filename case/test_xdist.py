
# 在命令行执行用例时，通过参数-n设置并行启动的进程数量。还可以设置为auto，会依据当前设备的cpu数量执行。
# 还可以通过--dist参数，设置用例分组，同一个组内的用例会在同一个进程中执行。

# --dist=loadscope 同一个module或同一个class下的用例会分配为同一组，按class分组优先于module。
# --dist=loadfile 同一个.py文件中的用例会分配为同一组。

import pytest
from time import sleep


class TestCase1:

    @pytest.mark.parametrize('keyword', ['a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j'])
    def test_baidu_search(self, keyword):
        sleep(1)
        print(f'搜索关键字{keyword}')


class TestCase2:

    @pytest.mark.parametrize('user', ['user1', 'user2', 'user3', 'user4', 'user5','user6', 'user7', 'user8', 'user9', 'user10'])
    def test_login(self, user):
        sleep(1)
        print(f'用户{user}登录成功')


if __name__ == '__main__':
    # 不使用pytest-xdist运行
    # pytest.main(['-vs'])
    # 使用pytest-xdist运行
    pytest.main(['-s', '-v', '-n', '3'])
