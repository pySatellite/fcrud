import datetime

from pydantic import BaseModel
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter


class OrbitCreate(BaseModel):
    name: str
    date: datetime.datetime
    tle_id: int
    line1: str
    line2: str


class Orbit(OrbitCreate):
    id: int


def get_orbit_table(metadata):
    return sqlalchemy.Table(
        "orbits",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("tle_id", sqlalchemy.Integer),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("date", sqlalchemy.DateTime(timezone=True), default=datetime.datetime.utcnow),
        sqlalchemy.Column("line1", sqlalchemy.String),
        sqlalchemy.Column("line2", sqlalchemy.String),
    )


def get_orbit_router(database, metadata):
    return DatabasesCRUDRouter(
        schema=Orbit,
        create_schema=OrbitCreate,
        table=get_orbit_table(metadata),
        database=database
    )
