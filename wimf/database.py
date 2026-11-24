
import os   
from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine import URL

from wimf.config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DB,
    get_database_credentials,
)

MYSQL_USER, MYSQL_PASSWORD = get_database_credentials()


# DATABASE_URL = (
#    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
#    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
#)
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DB,
)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db():
    """Builds the table layout out-of-the-box (unchanged)"""
    SQLModel.metadata.create_all(engine)

