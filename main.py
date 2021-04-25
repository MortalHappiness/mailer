import os
import time
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from getpass import getpass

import config
from receivers import get_receivers

# ========================================

# Read letter content
with open("letter.txt") as fin:
    subject = next(fin)
    text = fin.read()

# Read attachments
attachments = list()
if not os.path.exists("attachments"):
    os.mkdir("attachments")
for path in os.listdir("attachments"):
    part = MIMEBase("application", "octet-stream")
    with open(path, "rb") as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={path}")
    attachments.append(part)

count = 0

with smtplib.SMTP(config.SERVER, config.PORT) as smtp:
    smtp.ehlo()
    if smtp.has_extn('STARTTLS'):
        smtp.starttls()
        smtp.ehlo()
    print("Successfully connected to SMTP server")
    password = getpass(prompt=f"Password for {config.SENDER}: ")
    smtp.login(config.SENDER, password)
    print("Successfully login to SMTP server")

    for receiver in get_receivers():
        message = MIMEMultipart()
        message["From"] = config.SENDER
        message["To"] = receiver
        message["Subject"] = subject
        message.attach(MIMEText(text, "plain"))
        for attachment in attachments:
            message.attach(attachment)
        print(f"Sending email to {receiver}")
        smtp.sendmail(config.SENDER, receiver, message.as_string())
        print(f"Successfully sending email to {receiver}")
        count += 1
        if count % config.BATCH == 0:
            print("\n{count} mails was successfully sent, "
                  "sleeping for {config.SLEEP_TIME} seconds...")
            time.sleep(config.SLEEP_TIME)

print(f"\n{count} letters was successfully sent")
