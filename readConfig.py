import os
import codecs
import configparser
import re
#获取配置文件路径
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")

class ReadConfig:
    def __init__(self):
        fd = open(configPath, encoding='utf-8')
        data = fd.read()
        #注释主要设置编码格式utf-8
        #  所谓BOM，全称是Byte Order Mark，它是一个Unicode字符，通常出现在文本的开头，
        #  用来标识字节序（Big/Little Endian），除此以外还可以标识编码（UTF-8/16/32）
        #删除bom
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()
        #创建对象
        self.cf = configparser.ConfigParser()
        #读取配置
        self.cf.read(configPath)

    #获取对应配置信息
    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    #设置headers头部信息 写入例如：
    #Content - Type
    #Authorization
    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
    #with 是try catch finally 捕获异常 精简版本
    # def get_url(self, name):
    #     value = self.cf.get("URL", name)
    #     return value

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


