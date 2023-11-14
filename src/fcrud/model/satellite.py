from pydantic import BaseModel
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter
import datetime


class SatelliteCreate(BaseModel):
    name: str
    launch_time: datetime.datetime
    latitude: float
    longitude: float
    angle: float
    owner_id: int
    rocket_id: int


class Satellite(SatelliteCreate):
    id: int


def get_satellite_table(metadata):
    return sqlalchemy.Table(
        "satellites",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("launch_time", sqlalchemy.DateTime),
        sqlalchemy.Column("latitude", sqlalchemy.Float),
        sqlalchemy.Column("longitude", sqlalchemy.Float),
        sqlalchemy.Column("angle", sqlalchemy.Float),
        sqlalchemy.Column("owner_id", sqlalchemy.Integer),
        sqlalchemy.Column("rocket_id", sqlalchemy.Integer),
    )


def get_satellite_router(database, metadata):
    return DatabasesCRUDRouter(
        schema=Satellite,
        create_schema=SatelliteCreate,
        table=get_satellite_table(metadata),
        database=database
    )
