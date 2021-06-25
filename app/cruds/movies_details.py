from abc import ABC, abstractmethod
from typing import List

from app.schemas import MovieDetailCreate, MovieDetailsGet
from db import models


class AbstractMoviesDetailsCrud(ABC):

    @abstractmethod
    def add(self, movie_schema: MovieDetailCreate):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> MovieDetailsGet:
        raise NotImplementedError


class MoviesDetailsCrud(AbstractMoviesDetailsCrud):
    def __init__(self, session):
        self.session = session

    def add(self, movie_schema: MovieDetailCreate, single_push: bool = True):
        movie_details_object: models.MovieDetails = models.MovieDetails(property_name=movie_schema.property_name,
                                                                        value=movie_schema.value,
                                                                        url=movie_schema.url,
                                                                        movie_id=movie_schema.movie_id)
        if single_push:
            self.session.add(movie_details_object)
        return movie_details_object

    def get(self, id_) -> MovieDetailsGet:
        return self.session.query(models.MovieDetails).filter(models.MovieDetails.id == id_).first()

    def get_by_movie_id(self, movie_id) -> List[models.MovieDetails]:
        return self.session.query(models.MovieDetails).filter(models.MovieDetails.movie_id == movie_id).all()

    def add_list(self, movie_schema_list: List[MovieDetailCreate]):
        movie_object_list: List[models.MovieDetails] = []
        for movie_schema in movie_schema_list:
            movie_object_list.append(self.add(movie_schema=movie_schema, single_push=False))
        self.session.add_all(movie_object_list)
