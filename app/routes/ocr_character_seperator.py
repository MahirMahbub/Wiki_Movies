from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from app.depends.db_depend import get_db
from app.utils import catch_not_implemented_exception
from db.models import User, fastapi_users

router = InferringRouter()


@cbv(router)
class Campaign:
    db: Session = Depends(get_db)
    user: User = Depends(fastapi_users.current_user(active=True, verified=True))

    @router.get("/")
    @catch_not_implemented_exception
    def get_hello(self):
        return self.user
