from typing import Optional
from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.api_key import APIKeyHeader, APIKey
from app.config import AppConfig
from app.utils import Utils
import requests
import os


security = HTTPBearer()


class TimezoneHelper:
    pass



class CurrentAccount:
    id: int


# def get_current_user(authorization: Optional[str] = Header(...)):
def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    if AppConfig.APP_ENVIRONMENT == AppConfig.ENV_LOCAL:
        return 10

        # token
    # scheme = authorization.scheme
    # token = authorization.credentials
    # now decode JWT token and get user_id
    token_data = Utils().decode_jwt_token(authorization.credentials)
    print(token_data)
    user_id_string = token_data.get("user_id")
    return user_id_string

#
# def get_current_account_web_form(api_key: APIKey = Security(APIKeyHeader(name="X-Account-Api-Key"))):
#     if AppConfig.APP_ENVIRONMENT == AppConfig.ENV_LOCAL:
#         model = CurrentAccount()
#         model.id = 1
#         return model
#
# def get_current_account_web_chat(api_key: APIKey = Security(APIKeyHeader(name="X-Account-Api-Key"))):
#     if AppConfig.APP_ENVIRONMENT == AppConfig.ENV_LOCAL:
#         model = CurrentAccount()
#         model.id = 1
#         return model