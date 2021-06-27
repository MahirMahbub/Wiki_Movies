from abc import ABC, abstractmethod
from typing import Union

from sqlalchemy.orm import Session

from app.schemas import DataLoaderGet
from db import models


class AbstractDataLoaderCrud(ABC):
    @abstractmethod
    def get(self, reference: Union[int, str]):
        raise NotImplementedError


class DataLoaderCrud(AbstractDataLoaderCrud):
    def __init__(self, session: Session):
        self.session: Session = session

    def get(self, activity_name: str) -> models.DataLoader:
        return self.session.query(models.DataLoader).filter(models.DataLoader.activity_name == activity_name).first()

    def update_status(self, activity_name: str, status: bool) -> int:
        return self.session.query(models.DataLoader).filter(models.DataLoader.activity_name == activity_name).update({
            "status": status
        })
