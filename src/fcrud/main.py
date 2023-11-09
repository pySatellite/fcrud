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
from fcrud.model.alarm import Alarm, AlarmCreate
from fcrud.utils.macgyver_knife import sort_and_extract


DATABASE_URL = "postgresql://brown:brown@nrt.fcrud-db.internal:5432/brown"
BASEURL = "http://localhost:8000"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()
potatoes = sqlalchemy.Table(
    "alarms",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("dag", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
)
metadata.create_all(bind=engine)


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
    "http://127.0.0.1",
    "https://satellite-info.web.app",
    "https://satellite-info.firebaseapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = DatabasesCRUDRouter(
    schema=Alarm,
    create_schema=AlarmCreate,
    table=potatoes,
    database=database
)


# @router.get('')
# def overloaded_get_all():
#     return 'My overloaded route that returns all the items'


app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping")
def call_ping():
    return {"ping": ping()}


@app.get("/checklist")
def checklists(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    """http://localhost:8000/alarms?_end=10&_order=ASC&_sort=id&_start=0
    """

    target_url = f'{BASEURL}/alarms'
    total = requests.get(target_url).json()
    total_count = len(total)

    content = sort_and_extract(
        total, order=_order, sort=_sort, start=_start, end=_end)

    response.headers.update({
        "Access-Control-Expose-Headers": "X-Total-Count",
        "X-Total-Count": str(total_count)
    })
    return content


@app.get("/checklist/{item_id}")
def read_checklist(item_id: int):
    target_url = f'{BASEURL}/alarms/{item_id}'
    get_one = requests.get(target_url).json()
    return get_one
