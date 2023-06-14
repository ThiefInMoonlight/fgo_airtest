# -*- encoding=utf8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

user = ""
auth = ""
mailSenderName = "fgo自动脚本"
charSet = "utf-8"


def sendRewardDropMail(nowNum):
    sendMail("目标奖励掉落","目标奖励掉落+1，已掉落{}张".format(nowNum))


def sendMail(subject,message):
    smtp = smtplib.SMTP_SSL()
    smtp.connect('smtp.qq.com', 465)

    message = MIMEText(message, "plain", charSet)
    message['from'] = Header(mailSenderName, charSet)
    message['to'] = Header(mailSenderName, charSet)
    message['subject'] = Header(subject, charSet)

    try:

        smtp.login(user, auth)
        smtp.sendmail(user, [user], message.as_string())
        smtp.quit()
    except smtplib.SMTPException as err:

        print("can not send the email")
        print(str(err))

