from typing import Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
    film_name: str
    years: str


class MovieCreate(MovieBase):
    awards: Optional[str] = None
    nomination: Optional[str] = None
    wikipedia_link: Optional[str] = ""

    class Config:
        orm_mode = True


class MovieGet(MovieCreate):
    class Config:
        orm_mode = True


class MovieDetailsBase(BaseModel):
    property_name: str
    value: str


class MovieDetailCreate(MovieDetailsBase):
    url: Optional[str] = ""
    movie_id: int


class MovieDetailsGet(MovieDetailCreate):
    class Config:
        orm_mode = True


class DataLoaderBase(BaseModel):
    activity_name: str
    status: bool


class DataLoaderGet(DataLoaderBase):
    id: int

    class Config:
        orm_mode = True
