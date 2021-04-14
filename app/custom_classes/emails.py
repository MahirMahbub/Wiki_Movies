import jwt
import os

from .create_email import send_email
from .email_body_generator import body



def invite_user_email(email, token):
    # print("encoded_jwt: ", jwt.decode(encoded_jwt), "User Id: ", user_id)
    link = r"{}user-confirmation?token=".format(os.getenv("WEBAPP_BASE_URL")) + token
    
    try:
        send_email(to_addr=email, subject="Confirm account invitation", body=body(link))
        return True
    except Exception as e:
        return False

    # http: // localhost: 3030 / verify - account / user - invitation / token[build
    # with account and user id with timestamp]
