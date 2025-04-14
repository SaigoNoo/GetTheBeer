from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
from smtplib import SMTP

from dotenv import load_dotenv

load_dotenv()


class Mail:
    def __init__(self, receiver: str, title: str, body: str):
        self.receiver = receiver
        self.title = title
        self.body = body
        self.server = getenv(key="SMTP_SERVER")
        self.port = int(getenv(key="SMTP_PORT"))
        self.source = getenv(key="SMTP_EMAIL")
        self.password = getenv(key="SMTP_PASSWORD")
        self.msg = MIMEMultipart()

    def __create(self):
        self.msg["From"] = self.source
        self.msg["To"] = self.receiver
        self.msg["Subject"] = self.title
        self.msg.attach(MIMEText(self.body, "html"))

    def send(self):
        self.__create()
        try:
            socket = SMTP(self.server, self.port)
            socket.starttls()
            socket.login(self.source, self.password)

            socket.sendmail(self.source, self.receiver, self.msg.as_string())
        except Exception as e:
            return e


class OpenMailHTML:
    @staticmethod
    def html_raw(file: str, **options):
        with open(file=f"mail_templates/{file}.html", mode="r", encoding="utf-8") as html:
            data = html.read()
        for [key, value] in options.items():
            data = data.replace(f"${key}$", value)
        return data
