import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import Encoders

from configs.config import GlobalConfigs as GC


# Set up crap for the attachments
files = GC.TMP_BASE_PATH
filenames = [os.path.join(files, f) for f in os.listdir(files)]
# print filenames


# Set up users for email
gmail_user = "fbarquero86@gmail.com"
gmail_pwd = "Northrom26213832fAbP"
recipients = ['abarquero@socialware.com', 'fbarquero86@gmail.com']


# Create Module
def mail(to, subject, text, attach):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    # get all the attachments
    for file in filenames:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()


# send itmes
# mail(recipients,
#    "Todays report",
#    "Test email Text",
#    filenames)
# #!/usr/bin/env python
# import os
import zipfile
#
print GC.RESULTS_BASE_PATH

import os
print os.listdir(GC.RESULTS_BASE_PATH)
print os.path.isdir("{}/results_2015.08.26_10.55.15".format(GC.RESULTS_BASE_PATH))
dirs = ["{}/{}".format(GC.RESULTS_BASE_PATH, d) for d in os.listdir(GC.RESULTS_BASE_PATH)
        if os.path.isdir("{}/{}".format(GC.RESULTS_BASE_PATH, d))]
latest_result = sorted(dirs, key=lambda x: os.path.getctime(x), reverse=True)[:1]



def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for ff in files:
            ziph.write(os.path.join(root, ff))

if __name__ == '__main__':
    zipf = zipfile.ZipFile("{}/{}".format(GC.RESULTS_BASE_PATH, 'Python.zip'), 'w')
    zipdir(latest_result[0], zipf)
    zipf.close()
