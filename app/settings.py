import os

SQLALCHEMY_DATABASE_URL = os.environ.get(
    key="SQLALCHEMY_DATABASE_URL",
    default="postgresql://postgres:1234@organia_db:5432/organia",
)
