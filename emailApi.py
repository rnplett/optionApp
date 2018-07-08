import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def textRoland(title, message):
    MY_ADDRESS = <<gmail email>>
    PASSWORD = <<gmail password>>
    email = <<SMS alert email>>

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = title

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)

    s.quit()
