import pandas as pd
from decouple import config as env_config
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists

from flexit.models import Base

DATABASE_URL = env_config("DATABASE_URL")

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    engine = create_engine(DATABASE_URL.rstrip("flexit_db"))
    engine.execution_options(isolation_level="AUTOCOMMIT").execute(
        "CREATE DATABASE flexit_db"
    )
    engine = create_engine(DATABASE_URL)


def increment_table(tablename: str, table_length: int):
    """Increment the primary key for future insertions."""
    foreign_key_name = {
        "categories": "category_id",
        "persons": "person_id",
        "shows": "show_id",
        "show_category_intersection": "id",
        "show_cast_intersection": "id",
    }[tablename]
    with Session(engine) as session:
        query = f"ALTER SEQUENCE {tablename}_{foreign_key_name}_seq RESTART WITH {table_length + 1}"
        print(query)
        session.execute(query)
        session.commit()


def provision_table(tablename: str):
    """Inject app initial data & reset primary keys."""
    with open(f"data/{tablename}.csv", "r") as file:
        df = pd.read_csv(file)
        df.to_sql(tablename, con=engine, index=False, if_exists="append")
        print(f"{tablename} has been loaded!")

        increment_table(tablename, len(df))


def init_db(force: bool = False):
    """Create the database, tables, and load corresponding data."""
    if force:
        Base.metadata.drop_all(bind=engine)
        print("Dropped all tables.")

    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("DONE!")

    print("Loading initial data into tables.")
    try:
        for tablename in Base.metadata.tables.keys():
            provision_table(tablename)
    except IntegrityError as e:
        print("Database already exists. Maybe you need to force it?")
        raise e

    print("Database load completed!")
