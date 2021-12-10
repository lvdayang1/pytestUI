import smtplib
import os.path as pth
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header


def sendEmail(title, from_name, from_address, to_address, serverport, serverip, username, password):
    msg = MIMEMultipart()
    msg['Subject'] = Header(title, 'utf-8')
    # 这里的to_address只用于显示，必须是一个string
    msg['To'] = ','.join(to_address)
    msg['From'] = from_name
    # 添加附件地址
    part = MIMEApplication(open(r'E:\py\szass_proposal\Result\result.html', 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="result.html")  # 发送文件名称
    msg.attach(part)

    try:
        s = smtplib.SMTP_SSL(serverip, serverport)
        s.login(username, password)
        # 这里的to_address是真正需要发送的到的mail邮箱地址需要的是一个list
        s.sendmail(from_address, to_address, msg.as_string())
        print('%s----发送邮件成功' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(err)
#()HEFEN_D = pth.abspath(pth.dirname(__file__))

def send_email():
    TO = ['yanglv@irissz.com']
    config = {
        "from": "yanglv@irissz.com",
        "from_name": '吕洋',
        "to": TO,
        "serverip": "smtp.exmail.qq.com",
        "serverport": "465",
        "username": "yanglv@irissz.com",
        "password": "******"  # QQ邮箱的密码
    }
    now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    title = "iris自动化测试报告" + now
    sendEmail(title, config['from_name'], config['from'], config['to'], config['serverport'], config['serverip'],
              config['username'], config['password'])

#send_email()