import os

from sqlalchemy.orm import Session

from db.database import SessionLocal


class DbData:
    def __init__(self):
        self.root_directory: str = "db_merge_scripts"
        self.scripts = [
            "loader.sql"
        ]

    def sync(self, db: Session):
        for script in self.scripts:
            try:
                directory = os.path.join(self.root_directory, script)
                print(directory)
                sql = open(directory, "r").read()
                db.execute(sql)
                db.commit()
                print(greed("Data file processed: " + directory))
            except Exception as e:
                print(red("Error to process data file: " + directory))
                print(e)


def colored(text, r, g, b):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def red(text):
    return colored(text, 255, 0, 0)


def greed(text):
    return colored(text, 0, 255, 0)


def add_master_data():
    db = SessionLocal()
    DbData().sync(db)
    db.close()
