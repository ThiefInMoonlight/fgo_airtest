# -*- encoding=utf8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

user = ""
auth = ""


def sendRewardDropMail(nowNum):
    smtp = smtplib.SMTP_SSL()
    smtp.connect('smtp.qq.com', 465)

    message = MIMEText("目标奖励掉落+1，已掉落{}张".format(nowNum), "plain", "utf-8")
    message['from'] = Header("fgo自动脚本", "utf-8")
    message['to'] = Header("fgo自动脚本", "utf-8")
    subject = "目标奖励掉落"
    message['subject'] = Header(subject, "utf-8")

    try:

        smtp.login(user, auth)
        smtp.sendmail(user, [user], message.as_string())
        smtp.quit()
    except smtplib.SMTPException as err:

        print("can not send the email")
        print(str(err))

