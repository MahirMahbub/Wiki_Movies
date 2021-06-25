from sqlalchemy import Boolean, Column, Integer, String

from db.database import Base


class DataLoader(Base):
    __tablename__ = "data_loader"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_name = Column(String, nullable=False)
    status = Column(Boolean, default=False)


class MovieListData(Base):
    __tablename__ = "movie_list_data"
    id = Column(Integer, primary_key=True, index=True)
    film_name = Column(String, index=True)
    years = Column(String, index=True)
    awards = Column(String)
    nomination = Column(String)
    wiki_url = Column(String)


class MovieDetails(Base):
    __tablename__ = "movie_details"
    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String, index=True)
    value = Column(String, nullable=True)
    url = Column(String, nullable=True)
    movie_id = Column(Integer)  # Type MovieListData
