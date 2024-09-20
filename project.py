import os
import re
import PIL
import configparser
from fpdf import FPDF
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
class Card:
    def __init__(self, sender, receiver, email = None, congrats = None):
        self._sender = sender
        self._receiver = receiver
        self.email = email
        self._congrats = congrats
        self._pdf_card = None

    def __str__(self):
        return f"From {self.sender} to {self. receiver}"
    @property
    def sender(self):
        return self._sender
    @property
    def receiver(self):
        return self._receiver
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        matches = re.search(r"^(\w+\.)?\w+@(\w+\.)?\w+\.(edu|com|kz|ru)$", email)
        if matches:
            self._email = email
        else:
            self._email = None
    @property
    def congrats(self):
        return self._congrats
    @classmethod
    def get(cls):
        sender = input("From: ")
        receiver = input("To: ")
        email = input("Reciever's email: ")
        congrats = input("congratulation text: ")
        return cls(sender,receiver, email, congrats)

def main():
    card = Card.get()

    path = input("Path to photo, if you want customized card: ")
    filename = get_filename()
    if make_pdf(card.sender, card.receiver, card.congrats, path, filename):
        print("pdf successfully created")
        if card.email:
            print(send_myemail(card.sender, card.email, card.receiver,filename))
    else:
        print("something went wrong")

def get_filename():
    cwd = os.getcwd()
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if
    os.path.isfile(os.path.join(cwd, f))]
    max_number = []
    for i in range(len(onlyfiles)):
        matches = re.search(r"card(\d+)\.pdf", onlyfiles[i])
        if matches:
            max_number.append(int(matches.group(1)))
    if max_number:
        file_number = str(max(max_number) + 1)
    else:
        file_number = "1"

    filename = "card" + file_number + ".pdf"
    return filename

def make_pdf(s, r, congrats, p, fn):
    pdf = FPDF(orientation="L", unit = "mm", format = "A5")
    pdf.add_page()
    pdf.set_font("times", style="bi", size = 22)
    pdf.cell(185,130, border = 1, align ="C", new_x="LMARGIN", new_y="TOP")
    pdf.cell(185,8, f"From: {s}", align ="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(185,15, f"To: {r}", align ="C", new_x="LMARGIN", new_y="NEXT")
    try:
        pdf.image(p, h=pdf.eph-35, w=pdf.epw-35, x = pdf.epw/2-70)
    except (PIL.UnidentifiedImageError, FileNotFoundError):
        pass
        pdf.image("https://cataas.com/cat?type=medium&position=center&height=200", h=pdf.eph-35, w=pdf.epw-35, x = pdf.epw/2-70)
    pdf.set_font("times", style="i", size = 12)
    pdf.cell(185,10, f"{congrats[0:60]}", align ="C", new_x="LMARGIN", new_y="NEXT")
    if len(congrats) > 60:
        pdf.cell(185,10, f"{congrats[61:]}", align ="C", new_x="LMARGIN", new_y="NEXT")
    try:
        pdf.output(fn)
        return True
    except:
        return False

def send_myemail(s, email_to, r, fn):
    config = configparser.ConfigParser()
    config.read('config.ini')

    sender_email = config['EMAIL']['User']
    sender_password = config['EMAIL']['Password']

    subject = 'Congratulations'
    body = f"""From {s} to {r}
    The postcard was created using the CatCard service"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment= open(fn, 'rb')

    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + fn)
    msg.attach(attachment_package)
    text = msg.as_string()
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, sender_password)
    try:
        server.sendmail(sender_email, email_to, text)
        return "Card successfully sended"
    except:
        return "Card sending error"


if __name__ == "__main__":
    main()
