from pydantic import BaseModel
import sqlalchemy
from fastapi_crudrouter import DatabasesCRUDRouter


class AlarmCreate(BaseModel):
    dag: str
    email: str


class Alarm(AlarmCreate):
    id: int


def get_alarm_table(metadata):
    alarms_table = sqlalchemy.Table(
        "alarms",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("dag", sqlalchemy.String),
        sqlalchemy.Column("email", sqlalchemy.String),
    )
    return alarms_table


def get_alarm_router(database, metadata):
    alarm_router = DatabasesCRUDRouter(
        schema=Alarm,
        create_schema=AlarmCreate,
        table=get_alarm_table(metadata),
        database=database
    )
    return alarm_router
