"""App Utilities functions"""

from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status



class Utils:

    # This will yield start and end of week (from Sunday to Saturday)
    @staticmethod
    def get_start_and_end_date_for_current_week():
        day = datetime.utcnow().strftime("%Y-%m-%d")
        dt = datetime.strptime(day, '%Y-%m-%d')
        start = dt - timedelta(days=dt.weekday() + 1)
        end = start + timedelta(days=6)
        return {
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d")
        }


    @staticmethod
    def get_current_date_utc():
        return datetime.utcnow().strftime("%Y-%m-%d")


    @staticmethod
    def decode_jwt_token(token: str):
        from fastapi import HTTPException

        try:
            return jwt.decode(token, algorithms=['HS256'], verify=False)
        except jwt.ExpiredSignatureError:
            # Signature has expired
            raise HTTPException(
                status_code=401,
                detail="Token has been expired! Provide a valid token"
            )
        except jwt.exceptions.DecodeError:
            # Invalid JWT
            raise HTTPException(
                status_code=401,
                detail="Not a valid JWT Token!"
            )



def catch_not_implemented_exception(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(self, *args, **kw):
        try:
            return fn(self, *args, **kw)
        except NotImplementedError:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                detail="Method Not Implemented Yet")


    return wrapper
