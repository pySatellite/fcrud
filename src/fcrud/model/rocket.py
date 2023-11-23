from pydantic import BaseModel
import sqlalchemy
from sqlalchemy.dialects.postgresql import JSONB
from fastapi_crudrouter import DatabasesCRUDRouter
from typing import List, Dict, Union


class Engine(BaseModel):
    number: int
    name: str


class RocketCreate(BaseModel):
    name: str
    country: str
    thrust: float
    payload: float
    engines: List[Engine]
    # engines: List[Dict[str, Union[int, str]]]  # 수정된 부분


class Rocket(RocketCreate):
    id: int


def get_rocket_table(metadata):
    return sqlalchemy.Table(
        "rockets",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("country", sqlalchemy.String),
        sqlalchemy.Column("thrust", sqlalchemy.Float),
        sqlalchemy.Column("payload", sqlalchemy.Float),
        sqlalchemy.Column("engines", JSONB),
    )


def get_rocket_router(database, metadata):
    return DatabasesCRUDRouter(
        schema=Rocket,
        create_schema=RocketCreate,
        table=get_rocket_table(metadata),
        database=database
    )
