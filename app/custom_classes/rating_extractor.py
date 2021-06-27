from pprint import pprint
from typing import List, Union, Tuple, Dict, Set

import pandas as pd
from pandas import DataFrame, Series
from sqlalchemy.orm import Session

from app.cruds.movies_list import MoviesDataCrud
from app.custom_classes.data_loader.handler.movie_list_handler import MovieListHandler


class RatingExtractor():
    def __init__(self, session: Session):
        self.__session: Session = session

    def execute(self) -> None:
        movies, rating, movies_basic_data = RatingExtractor.data_reader()
        movies: DataFrame = RatingExtractor.movie_name_year_extractor(movies)
        movies_basic_data = RatingExtractor.extract_optional_year(movies_basic_data)
        existing_movies_join = pd.merge(movies_basic_data, movies, left_on=["Film", "Year"], right_on=["title", "year"],
                                        how='inner')
        final_common_movie_and_rating = pd.merge(existing_movies_join, rating, on="movieId", how='inner')
        movie_rating_data_list = RatingExtractor.rating_and_rater_extractor(final_common_movie_and_rating)
        self.data_writer(movie_rating_data_list)

    @staticmethod
    def rating_and_rater_extractor(final_common_movie_and_rating: DataFrame) -> List[Dict[str, Union[str, int, float]]]:
        film_name_list: Set[str] = set(final_common_movie_and_rating["Film"].tolist())
        movie_rating_data: List[Dict[str, Union[str, int, float]]] = []
        for film_name in film_name_list:
            print("Extracting rating for: ", film_name)
            rows: Series = final_common_movie_and_rating.loc[final_common_movie_and_rating['Film'] == film_name]
            count_user: int = rows.shape[0]
            rating_sum: int = rows["rating"].sum(axis=0)
            avg_rating: float = rating_sum / count_user
            # print(film_name, count_user, rating_sum, avg_rating)
            movie_rating_data.append({
                "film": film_name,
                "total_user_rated": count_user,
                "average_rating": avg_rating
            })
        return movie_rating_data

    @staticmethod
    def extract_optional_year(movies_basic_data: DataFrame) -> DataFrame:
        new_movies_basic_data: List[List[Union[int, str]]] = []
        for index, row in movies_basic_data.iterrows():
            if "/" in row["Year"]:
                year1, year2 = row["Year"].split("/")
                year2 = year1[0:2] + year2
                row2 = row.copy(deep=True)
                row2["Year"] = year2
                row["Year"] = year1
                new_movies_basic_data.append(row2.to_list())
            new_movies_basic_data.append(row.to_list())
        new_movies_basic_data: DataFrame = pd.DataFrame(new_movies_basic_data,
                                                        columns=['Film', 'Year', 'Awards', 'Nominations', 'Wiki Link',
                                                                 'id'])

        return new_movies_basic_data

    @staticmethod
    def data_reader() -> Tuple[DataFrame, DataFrame, DataFrame]:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        movies_basic_data: DataFrame = MovieListHandler().execute(
            request_data=f"https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films", is_dataframe=True)
        rating: DataFrame = pd.read_csv(r'https://school.cefalolab.com/assignment/python/ratings.csv')
        movies: DataFrame = pd.read_csv(r'https://school.cefalolab.com/assignment/python/movies.csv')
        return movies, rating, movies_basic_data

    @staticmethod
    def movie_name_year_extractor(movies: DataFrame) -> DataFrame:
        movie_name_with_year_list = movies["title"].tolist()
        movie_name_list: List[str] = []
        movie_year_list: List[str] = []
        for movie_name_with_year in movie_name_with_year_list:
            movie_name_list.append(movie_name_with_year[:-7])
            movie_year_list.append(movie_name_with_year[-5:-1])
        movies["title"] = movie_name_list
        movies["year"] = movie_year_list
        return movies

    def data_writer(self, movie_rating_data_list: List[Dict[str, Union[str, int, float]]]) -> None:
        for movie_rating_data in movie_rating_data_list:
            MoviesDataCrud(self.__session).update_rating_and_rater(film_name=movie_rating_data["film"],
                                                                   rating=movie_rating_data["average_rating"],
                                                                   rater=movie_rating_data["total_user_rated"])

            self.__session.commit()
