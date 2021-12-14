# pytest插件
# 用例依赖 pip install pytest-dependency
# 失败重跑 pip install pytest-rerunfailures
# 指定用例执行顺序 pip install pytest-ordering
# 多重断言 pip install pytest-assume
import pytest
import random

class TestCase:

    # 通过装饰器@pytest.mark.dependency()标记当前用例为被依赖用例，被依赖用例需要优先关联用例执行
    @pytest.mark.dependency()
    def test_01(self):
        print("测试用例01，执行失败")
        assert 1 == 2

    # 通过使用装饰器关联被依赖用例，通过depends参数指定用例名称关联用例
    @pytest.mark.dependency(depends=['test_01'])
    def test_02(self):
        print("测试用例02，跳过")

    # 标记被依赖用例时，可以通过name参数指定别名
    @pytest.mark.dependency(name="func_2")
    def test_03(self):
        print("测试用例03，执行成功！")

    # 使用depends参数指定定义的别名关联用例
    @pytest.mark.dependency(depends=['func_2'])
    def test_04(self):
        print("测试用例04，执行成功！")

    # depends参数可以关联多个测试用例，使用“,”分隔即可
    @pytest.mark.dependency(depends=['test_01', 'func_2'])
    def test_05(self):
        print("测试用例05，跳过")

    # 使用装饰器设置用例失败后的重新执行最大次数和每次执行的间隔时间（单位：秒）
    # --reruns 重新执行最大次数 --reruns-delay 间隔时间。
    @pytest.mark.dependency(depends=['func_2'])
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_06(self):
        result = random.choice(['a', 'b', 'c', 'd', 'e'])
        print(f"result={result}")
        assert result == 'c'

    def test_07(self):
        print("测试用例07")

    def test_08(self):
        print("测试用例08")

    # 使用装饰器设置执行顺序为2
    @pytest.mark.run(order=2)
    def test_09(self):
        print("测试用例09，执行顺序为2")

    # 使用装饰器设置执行顺序为1
    @pytest.mark.run(order=1)
    def test_10(self):
        print("测试用例10，执行顺序为1")

    # 使用assert断言
    def test_11(self):
        print("断言1")
        assert 1 == 1
        print('断言2')
        assert 2 == 1
        print("断言3")
        assert 3 == 3
        print('用例结束')

    # 使用pytest.assume()多重断言
    def test_12(self):
        print('断言1')
        pytest.assume(1 == 1)
        print('断言2')
        pytest.assume(2 == 1)
        print('断言3')
        pytest.assume(3 == 3)
        print('用例结束')

if __name__ == '__main__':
    pytest.main(['-vs'])
