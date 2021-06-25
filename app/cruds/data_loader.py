from abc import ABC, abstractmethod
from typing import Union

from app.schemas import DataLoaderGet
from db import models


class AbstractDataLoaderCrud(ABC):
    @abstractmethod
    def get(self, reference: Union[int, str]) -> DataLoaderGet:
        raise NotImplementedError


class DataLoaderCrud(AbstractDataLoaderCrud):
    def __init__(self, session):
        self.session = session

    def get(self, activity_name: str):
        return self.session.query(models.DataLoader).filter(models.DataLoader.activity_name == activity_name).first()

    def update_status(self, activity_name: str, status: bool):
        return self.session.query(models.DataLoader).filter(models.DataLoader.activity_name == activity_name).update({
            "status": status
        })
