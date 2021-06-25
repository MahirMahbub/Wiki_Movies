from app.custom_classes.data_loader.handler.movie_details_handler import MovieDetailsHandler
from app.custom_classes.data_loader.handler.movie_list_handler import MovieListHandler


class CreateData(object):
    __instance__ = None

    def __init__(self):
        if CreateData.__instance__ is None:
            CreateData.__instance__ = self
        else:
            raise Exception("You cannot create another WebFormSocketManager class")

    @staticmethod
    def get_instance():
        if not CreateData.__instance__:
            CreateData()
        return CreateData.__instance__

    def get_chain_of_responsibility(self):
        movie_list = MovieListHandler()
        movie_details = MovieDetailsHandler()
        movie_details.set_prev(movie_list)
        movie_details.handle(f"https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")



