# -*-coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime


def send_email(receivers):
    mail_host = 'smtp.163.com'
    mail_user = '13122780440'
    mail_pass = 'AMGSBPKLBPDHIJWD'
    sender = '13122780440@163.com'
    # message = MIMEText('content', 'plain', 'utf-8')
    message = MIMEMultipart()
    # message['Subject'] = '赣服通审核'
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = Header('赣服通审核', 'utf-8')
    xlsx = MIMEApplication(
        open('/home/zg/Downloads/selenium/gft/应用及接口审核上架申请表.xlsx', 'rb').read())
    xlsx["Content-Type"] = 'application/octet-stream'
    xlsx.add_header('Content-Disposition',
                    'attachment',
                    filename='应用及接口审核上架申请表.xlsx')
    message.attach(xlsx)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)


if __name__ == '__main__':
    # receivers = ['604328914@qq.com']
    print(datetime.now())
    receivers = ['luochenlu@digital-jx.com']
    send_email(receivers)