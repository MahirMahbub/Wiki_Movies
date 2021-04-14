import os

import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from db.query_helper import CustomQuery
from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

# app and db both on local
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# app on loal and db on docker
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:secret@127.0.0.1:6001/postgres?sslmode=prefer"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, pool_size=3, max_overflow=0
# )

# app and db both on docker
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:secret@db_campaign:5432/postgres?sslmode=prefer"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, pool_size=3, max_overflow=0
# )

# app and db both on docker use .env file

host_server = os.getenv('DB_HOST_SERVER')
db_server_port = os.getenv('DB_SERVER_PORT')
database_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_ssl_mode = os.getenv('DB_SSL_MODE')
SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server,
                                                                          db_server_port, database_name, db_ssl_mode)
# print(SQLALCHEMY_DATABASE_URL)
DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=3, max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, query_cls=CustomQuery)
database = databases.Database(SQLALCHEMY_DATABASE_URL)
Base: DeclarativeMeta = declarative_base()

# Base.metadata.create_all(engine)
