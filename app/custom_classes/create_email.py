import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def create_email(from_addr, to_addr, subject, body, file_path="", type_=None):
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = from_addr

    # storing the receivers email address
    msg['To'] = to_addr

    # storing the subject
    msg['Subject'] = subject

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'html'))

    # open the file to be sent
    if not file_path == "":
        attachment = open(file_path, "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)
        extension = file_path.split("/")[-1].split(".")[-1]
        if type_ == "Contact":
            file_name = "Export_contact_data" + "." + extension
        elif type_ == "Company":
            file_name = "Export_company_data" + "." + extension
        else:
            file_name = "ADN_file"+"." + extension
        p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
    return msg.as_string()



def send_email(to_addr, subject, body, file_name="", type_=""):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    # server = smtplib.SMTP(smtp_host, smtp_port)
    try:
        server.login(os.getenv("FROM_EMAIL"), os.getenv("EMAIL_PASSWORD"))
        text = create_email(from_addr=os.getenv("FROM_EMAIL"),
                            to_addr=to_addr,
                            body=body,
                            subject=subject,
                            file_path=file_name,
                            type_=type_)
        server.sendmail(os.getenv("FROM_EMAIL"), to_addr, text)
        server.close()
        return True
    except Exception as e:
        # print(e)
        return False
