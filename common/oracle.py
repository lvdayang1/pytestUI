import cx_Oracle as cx
import readConfig
from common.log import Logg
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

localReadConfig = readConfig.ReadConfig()
class MyDB(object):
    global host, username, password, port, database, hosts, config
    host = localReadConfig.get_db("host")
    username = localReadConfig.get_db("username")
    password = localReadConfig.get_db("password")
    port = localReadConfig.get_db("port")
    database = localReadConfig.get_db("database")
    hosts = host + ":" + port + "/" + database
    def __init__(self):
        self.log = Logg()
        self.logger = Logg().get_logger()
        self.db = None
        self.cursor = None
        self.con = self.connectDB()

    def connectDB(self):
        # 数据库连接重试功能和连接超时功能的DB连接
        _conn_status = True
        while _conn_status :
            try:
                print("连接数据库中..")
                conn = cx.connect(username, password, hosts)
                print("Connect DB successfully!")
                _conn_status = False  # 如果conn成功则_status为设置为False则退出循环，返回db连接对象
                return conn
            except ConnectionError as ex:
                self.logger.error(str(ex))
            continue

    def executeSql(self, sql):
        # con = self.connectDB()
        self.cursor = self.con.cursor()
        self.cursor.execute(sql)
        self.con.commit()
        return self.cursor

    def getAll(self, cursor):
        value = cursor.fetchall()
        return value

    def getOne(self, cursor):
        value = cursor.fetchone()
        return value

    def closeDB(self):
        self.con.close()
        print("Database closed")