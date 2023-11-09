from pydantic import BaseModel


class AlarmCreate(BaseModel):
    dag: str
    email: str


class Alarm(AlarmCreate):
    id: int
