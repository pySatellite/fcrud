from typing import Union

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import databases
import sqlalchemy
import requests

from fcrud.echo.ping import ping
from fcrud.model.alarm import get_alarm_router
from fcrud.model.airflow import get_airflow_router
from fcrud.utils.macgyver_knife import sort_and_extract


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
    "https://satellite-info.web.app",
    "https://satellite-info.firebaseapp.com",
    "https://satellite.diginori.com/",
    "https://sli.diginori.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://brown:brown@nrt.fcrud-db.internal:5432/brown"
LOCAL_API_BASE_URL = "http://localhost:8000"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app.include_router(get_alarm_router(database, metadata))
app.include_router(get_airflow_router(database, metadata))

metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping")
def call_ping():
    return {"ping": ping()}


def read_json_server_provider(resource: str, _end: int, _order: str, _sort: str, _start: int, response: Response):
    target_url = f'{LOCAL_API_BASE_URL}/{resource}'
    total = requests.get(target_url).json()
    total_count = len(total)
    content = sort_and_extract(
        total, order=_order, sort=_sort, start=_start, end=_end)

    response.headers.update({
        "Access-Control-Expose-Headers": "X-Total-Count",
        "X-Total-Count": str(total_count)
    })
    return content


@app.get("/alarms_ra")
def alarms_ra(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    return read_json_server_provider("alarms", _end, _order, _sort, _start, response)


@app.get("/airflows_ra")
def airflows_ra(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    return read_json_server_provider("airflows", _end, _order, _sort, _start, response)
