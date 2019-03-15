import smtplib
from email.mime.text import MIMEText

def SendEmail(data):  # 发送邮件

    try:
        msg_from = 'renshareck@aliyun.com'
        passwd = 'passwd'
        msg_to = 'renshareck@163.com'
        subject = "OK!Shareck!"
        content1 = data
        content2 = "\n"
        content = content1 + content2

        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        email = smtplib.SMTP_SSL("smtp.aliyun.com", 465)
        email.login(msg_from, passwd)
        email.sendmail(msg_from, msg_to, msg.as_string())
        email.quit()
        print("Send End!")
    except:
        print("Send error!")

if __name__ == "__main__":
    SendEmail("I have got it !")