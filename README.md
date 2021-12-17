pytest+selenium
UI自动化测试框架使用说明
项目目录

common：存放公共方法，如封装的selenium方法等
pages：存放获取页面元素及元素操作的方法
conftest.py：在测试套件中的所有测试用例之间的共享方法
config.ini：一些配置信息，如数据库信息，邮件信息等
ptyest.ini：allurereport配置信息
readConfig.py：获取config.ini内容方法
requirement.txt：相关版本信息
run_all.py：运行所有用例及发送邮件

common文件夹,pytest.ini,readConfig.py,requirement.txt,run_all.py无需修改
pages和case用来写测试用例，根据需要添加

conftest.py
把需要共享的文件添加相应的fixture方法


config.ini
可以把需要配置的信息放在这里，这里如果添加了相应的信息，需要在readConfig.py写入相关get方法

用例执行
命令行输入  python run_all.py

