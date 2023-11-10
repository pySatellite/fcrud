from pydantic import BaseModel
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter


class AirflowCreate(BaseModel):
    name: str
    cron: str


class Airflow(AirflowCreate):
    id: int


def get_airflow_table(metadata):
    airflow_table = sqlalchemy.Table(
        "airflows",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("cron", sqlalchemy.String),
    )
    return airflow_table


def get_airflow_router(database, metadata):
    airflow_router = DatabasesCRUDRouter(
        schema=Airflow,
        create_schema=AirflowCreate,
        table=get_airflow_table(metadata),
        database=database
    )
    return airflow_router
