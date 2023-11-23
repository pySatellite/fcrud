from pydantic import BaseModel
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter


class OwnerCreate(BaseModel):
    name: str


class Owner(OwnerCreate):
    id: int


def get_rocket_table(metadata):
    return sqlalchemy.Table(
        "owners",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
    )


def get_owner_router(database, metadata):
    return DatabasesCRUDRouter(
        schema=Owner,
        create_schema=OwnerCreate,
        table=get_rocket_table(metadata),
        database=database
    )
