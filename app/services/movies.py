import logging
import re
from typing import List, Dict, Any

import humps
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy_pagination import paginate
from starlette import status

from app.cruds.movies_details import MoviesDetailsCrud
from app.cruds.movies_list import MoviesDataCrud
from db import models


class Movies(object):

    def get_paginated_movies_list(self, db, count, page):
        try:
            crud_movies_list_object = MoviesDataCrud(session=db)
            movie_data_query_object = crud_movies_list_object.get_query()
            __pagination_obj = paginate(movie_data_query_object, page=page, page_size=count)
        except AttributeError as e:
            logging.exception("Attribute Error occurred")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=str(e))

        if __pagination_obj:
            try:
                __pagination_obj.items = self.__get_paginated_movies_list_with_movie_details(
                    db=db,
                    movie_data_list=__pagination_obj.items)

                return {
                    'found': True if __pagination_obj.items else False,
                    'items': __pagination_obj.items,
                    'nextPage': __pagination_obj.next_page,
                    'previousPage': __pagination_obj.previous_page,
                    'totalItems': __pagination_obj.total,
                    'pages': __pagination_obj.pages,
                    'hasNext': __pagination_obj.has_next,
                    'hasPrevious': __pagination_obj.has_previous
                }
            except Exception as e:
                logging.exception("Error occurred")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Error occurred")
        else:
            logging.exception("Pagination failed")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Pagination failed")

    def get_movies_detail_info(self, db: Session, id_: int):
        crud_movies_list_object = MoviesDataCrud(session=db)
        __movie_data = crud_movies_list_object.get(id_=id_)
        if __movie_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No movie with specified id has been found")
        try:
            return self.__get_manipulated_movie_info(db, __movie_data, id_)
        except Exception as e:
            logging.exception("Error Occurred")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Error occurred")

    def __get_paginated_movies_list_with_movie_details(self, movie_data_list: List[Dict[str, Any]], db: Session):
        movie_details_data_list: List[Dict[str, Any]] = []
        for movie_data in movie_data_list:
            movie_id: int = movie_data.id
            movie_dict = self.__get_manipulated_movie_info(db, movie_data, movie_id)
            movie_details_data_list.append(movie_dict)
        return movie_details_data_list

    def __get_manipulated_movie_info(self, db, movie_data, movie_id):
        movie_details: List[models.MovieDetails] = MoviesDetailsCrud(db).get_by_movie_id(movie_id)
        movie_dict = self.__data_maker(movie_data=movie_data, movie_details=movie_details)
        return movie_dict

    @staticmethod
    def __data_maker(movie_data: models.MovieData, movie_details: List[models.MovieDetails]):
        __movie_data = {humps.camelize(k): v for k, v in jsonable_encoder(movie_data).items()}
        property_names = [movie_detail.property_name for movie_detail in movie_details]
        __data_details = {humps.camelize(property_name): [] for property_name in property_names}
        for movie_detail in movie_details:
            __data_details[humps.camelize(movie_detail.property_name)].append({
                "value": re.sub(r'\[[1-100]\]', '', movie_detail.value),
                "url": movie_detail.url
            })
        __movie_data.update(__data_details)

        return __movie_data
