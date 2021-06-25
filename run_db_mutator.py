from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from db.models import Base
import os, shutil 
import glob


def create_all():
    Base.metadata.create_all(bind=engine)


def drop_all():
    Base.metadata.drop_all(bind=engine)


def drop_db_version():
    db = SessionLocal()
    db.execute("DROP TABLE IF EXISTS alembic_version")
    db.commit()
    db.close()


def remove_local_migrations():
    # https://stackoverflow.com/questions/31392285/clear-postgresql-and-alembic-and-start-over-from-scratch
    files = glob.glob('db_migrations/versions/*.py')
    for f in files:
        os.remove(f)

       
def apply_migations():
    os.system("alembic upgrade head")

def create_migration():
    os.system("alembic revision --autogenerate")

def create_migrations_and_apply():
    os.system("alembic revision --autogenerate")
    apply_migations()
 

def scratch():
    drop_all()
    drop_db_version()


def auto():
    drop_db_version()
    remove_local_migrations()
    create_migrations_and_apply()


if __name__ == "__main__":
    # from_scratch_auto()
    auto()