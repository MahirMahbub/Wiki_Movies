from abc import ABC, abstractmethod

from sqlalchemy.orm import Query, Session

from app.schemas import MovieCreate, MovieGet
from db import models


class AbstractMoviesDataCrud(ABC):

    @abstractmethod
    def add(self, movie_schema: MovieCreate):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference):
        raise NotImplementedError


class MoviesDataCrud(AbstractMoviesDataCrud):
    def __init__(self, session: Session):
        self.session = session

    def add(self, movie_schema: MovieCreate) -> models.MovieData:
        movie_object: models.MovieData = models.MovieData(film_name=movie_schema.film_name,
                                                          years=movie_schema.years,
                                                          wiki_url=movie_schema.wikipedia_link,
                                                          awards=movie_schema.awards,
                                                          nomination=movie_schema.nomination
                                                          )
        self.session.add(movie_object)
        self.session.flush()
        return movie_object

    def get(self, id_: int) -> models.MovieData:
        return self.session.query(models.MovieData).filter(models.MovieData.id == id_).first()

    def get_by_film_name(self, film_name: str) -> models.MovieData:
        return self.session.query(models.MovieData).filter(models.MovieData.film_name == film_name).first()

    def get_query(self) -> Query:
        return self.session.query(models.MovieData)

    def update_rating_and_rater(self, rating: float, rater: int, film_name: str) -> int:
        return self.session.query(models.MovieData).filter(models.MovieData.film_name == film_name).update({
            "average_rating": rating,
            "number_of_rater": rater
        })
