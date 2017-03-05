import smtplib
from login import login_info # saved Username and Password
from types import *
from os.path import basename
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEText import MIMEText
from email.utils import COMMASPACE, formatdate

def send_email(send_from, send_to, cc, bcc, subject, text, login_info={}, files=None,
              server="smtp.gmail.com", port="587"):
    assert isinstance(send_to, list)
    assert isinstance(cc, list)
    assert isinstance(bcc, list)
    assert type(send_from) is StringType, "send_from is not a String: %r" % send_from

    # define msg
    msg = MIMEMultipart()
    msg['From'] = send_from.split('@')[0]
    msg['To'] = COMMASPACE.join(send_to)
    msg['Cc'] = COMMASPACE.join(cc)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    # msg body
    msg.attach(MIMEText(text))
    # attachment
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(),Name=basename(f))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    mailserver = smtplib.SMTP(server, port)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(login_info['Username'], login_info['Password'])
    mailserver.sendmail(send_from, send_to + cc + bcc, msg.as_string())
    mailserver.quit()

send_from = "xiaoxiaobaojiang@gmail.com"
send_to = ["jessicawang910@gmail.com",]
cc = ["dongdong705@gmail.com",]
bcc = ["xiaoxiaobaojiang@gmail.com"]
subject = "Email with attachment by Python"
text = "Great job done!"
files = ["/Users/jessicawang910/Desktop/pig.png",]
send_email(send_from, send_to, cc, bcc, subject, text, login_info, files)