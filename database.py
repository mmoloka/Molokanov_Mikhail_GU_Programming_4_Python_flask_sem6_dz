import sqlalchemy
from sqlalchemy import create_engine
import databases

from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(settings.NAME_MAX_LENGTH)),
    sqlalchemy.Column("last_name", sqlalchemy.String(settings.NAME_MAX_LENGTH)),
    sqlalchemy.Column("email", sqlalchemy.String(settings.EMAIL_MAX_LENGTH)),
    sqlalchemy.Column("password", sqlalchemy.String(settings.PASSWORD_MAX_LENGTH))
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(settings.TITLE_MAX_LENGTH)),
    sqlalchemy.Column("description", sqlalchemy.String(settings.DESCRIPTION_MAX_LENGTH)),
    sqlalchemy.Column("price", sqlalchemy.Float())
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.Date()),
    sqlalchemy.Column("status", sqlalchemy.Boolean())
)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
