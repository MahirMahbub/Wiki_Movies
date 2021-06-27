import traceback
from typing import Any, KeysView
from typing import List, Dict

from sqlalchemy.orm import Session

from app.cruds.movies_details import MoviesDetailsCrud
from app.cruds.movies_list import MoviesDataCrud
from app.custom_classes.data_loader.handler.abstract_handler import AbstractHandler
from app.schemas import MovieCreate, MovieDetailCreate
from db import models
from db.database import SessionLocal


class DBHandler(AbstractHandler):
    def execute(self, request_data: List[Dict[str, Any]]) -> bool:
        movies_details_list, movies_basic_list = request_data
        db: Session = SessionLocal()
        for idx, movies_basic in enumerate(movies_basic_list):
            film_name = MoviesDataCrud(session=db).get_by_film_name(film_name=movies_basic.get("Film", True))
            if film_name:
                continue
            print("Pushing data for: ", movies_basic.get("Film"))
            movie_basic_schema: MovieCreate = MovieCreate(film_name=movies_basic.get("Film", ""),
                                                          years=movies_basic.get("Year", ""),
                                                          awards=movies_basic.get("Awards", ""),
                                                          nomination=movies_basic.get("Nominations", ""),
                                                          wikipedia_link=movies_basic.get("Wiki Link", "")
                                                          )
            movie_data: models.MovieData = MoviesDataCrud(session=db).add(movie_basic_schema)
            movie_id: int = movie_data.id
            movies_details: Dict[str, Any] = movies_details_list[idx]
            attributes_list: KeysView = movies_details_list[idx].keys()
            movie_schema_list: List[MovieDetailCreate] = []
            for attr in attributes_list:
                attr_data_list: Any = movies_details[attr]
                for attr_data in attr_data_list:
                    attr_data_schema: MovieDetailCreate = MovieDetailCreate(property_name=attr,
                                                                            value=attr_data["value"],
                                                                            url=attr_data["url"],
                                                                            movie_id=movie_id)
                    movie_schema_list.append(attr_data_schema)
            try:
                MoviesDetailsCrud(session=db).add_list(movie_schema_list=movie_schema_list)
                db.commit()
            except Exception as e:
                # logging.exception("SQLAlchemy Error")
                traceback.print_exc()
                db.rollback()
                return False
        return True

    def handle(self, request_data: Any):
        return super().handle(request_data)
