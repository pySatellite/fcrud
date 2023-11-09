from typing import Union

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from fastapi_crudrouter import DatabasesCRUDRouter

import databases
import sqlalchemy
import requests

from fcrud.echo.ping import ping
from fcrud.model.alarm import Alarm
from fcrud.utils.macgyver_knife import sort_and_extract


DATABASE_URL = "postgresql://brown:brown@nrt.fcrud-db.internal:5432/brown"
BASEURL = "http://localhost:8000"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
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

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/orions")
def potatoes(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    """http://localhost:8000/orions?_end=10&_order=ASC&_sort=id&_start=0
    """

    target_url = f'{BASEURL}/potatoes'
    total = requests.get(target_url).json()
    total_count = len(total)

    content = sort_and_extract(
        total, order=_order, sort=_sort, start=_start, end=_end)

    response.headers.update({
        "Access-Control-Expose-Headers": "X-Total-Count",
        "X-Total-Count": str(total_count)
    })
    return content
