from pydantic import BaseModel
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter
import datetime


class SatelliteCreate(BaseModel):
    name: str = "pySatellite-001"
    launch_time: datetime.datetime
    latitude: float = 37.4932385
    longitude: float = 126.9175228
    angle: float = 77.777
    owner_id: int = 1
    rocket_id: int = 1


class Satellite(SatelliteCreate):
    id: int


def get_satellite_table(metadata):
    return sqlalchemy.Table(
        "satellites",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("launch_time", sqlalchemy.DateTime(timezone=True), default=datetime.datetime.utcnow),
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
