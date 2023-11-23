from typing import Union

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

import databases
import sqlalchemy
import requests

from fcrud.model.owner import get_owner_router
from fcrud.model.rocket import get_rocket_router
from fcrud.model.satellite import get_satellite_router
from fcrud.model.orbit import get_orbit_router
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
    "http://localhost:5174",
    "https://satellite-info.web.app",
    "https://satellite-info.firebaseapp.com",
    "https://satellite.diginori.com",
    "https://sli.diginori.com",
    "https://satellite-info.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://brown:brown@nrt.fcrud-db.internal:5432/brown"
# DATABASE_URL = "mysql+pymysql://root:fcrud123456@localhost:3306/mysql"
LOCAL_API_BASE_URL = "http://localhost:8000"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app.include_router(get_satellite_router(database, metadata))
app.include_router(get_rocket_router(database, metadata))
app.include_router(get_owner_router(database, metadata))
app.include_router(get_orbit_router(database, metadata))

metadata.create_all(bind=engine)


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='https://satellite.diginori.com')


@app.get("/ping")
async def ping():
    return {"Hello": "World"}


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


@app.get("/satellites_ra")
def satellites_ra(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    return read_json_server_provider("satellites", _end, _order, _sort, _start, response)


@app.get("/rockets_ra")
def rockets_ra(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    return read_json_server_provider("rockets", _end, _order, _sort, _start, response)


@app.get("/owners_ra")
def owners_ra(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    return read_json_server_provider("owners", _end, _order, _sort, _start, response)

@app.get("/orbits_ra")
def orbits_ra(response: Response, _end: int = 10, _order: str = "ASC", _sort: str = "id", _start: int = 0):
    return read_json_server_provider("orbits", _end, _order, _sort, _start, response)
