from pydantic import BaseModel


class Alarm(BaseModel):
    id: int
    dag: str
    email: str
