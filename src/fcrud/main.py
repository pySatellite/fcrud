from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from fcrud.echo.ping import ping
from fcrud.model.alarm import Alarm

import databases
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter

from contextlib import asynccontextmanager


DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={
                                  "check_same_thread": False})
metadata = sqlalchemy.MetaData()
potatoes = sqlalchemy.Table(
    "potatoes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("thickness", sqlalchemy.Float),
    sqlalchemy.Column("mass", sqlalchemy.Float),
    sqlalchemy.Column("color", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
)
metadata.create_all(bind=engine)


class PotatoCreate(BaseModel):
    thickness: float
    mass: float
    color: str
    type: str


class Potato(PotatoCreate):
    id: int


@asynccontextmanager
async def life(app: FastAPI):
    # startup
    await database.connect()
    yield
    # shutdown
    await database.disconnect()


app = FastAPI(lifespan=life)


router = DatabasesCRUDRouter(
    schema=Potato,
    create_schema=PotatoCreate,
    table=potatoes,
    database=database
)
app.include_router(router)

app.include_router(CRUDRouter(schema=Alarm))


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping")
def call_ping():
    return {"ping": ping()}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
