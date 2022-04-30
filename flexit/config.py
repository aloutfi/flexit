from decouple import config as env_config
from sqlalchemy import create_engine

DATABASE_URL = env_config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
