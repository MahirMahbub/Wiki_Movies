from typing import Optional

from fastapi import FastAPI, Depends, Query, Path
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from app.depends.db_depend import get_db
from app.utils import catch_not_implemented_exception
from app.services.movies import Movies as movieService

app = FastAPI()
router = InferringRouter()



@cbv(router)
class Movies(object):
    db: Session = Depends(get_db)

    @router.get("/movies")
    @catch_not_implemented_exception
    def get_paginated_movies_list(self, count: Optional[int] = Query(20), page: Optional[int] = Query(1)):
        return movieService().get_paginated_movies_list(db=self.db, page=page, count=count)


    @router.get("/movie/{id_}")
    @catch_not_implemented_exception
    def get_detail_info_about_movie(self, id_: int =Path(...)):
        return movieService().get_movies_detail_info(db=self.db, id_=id_)