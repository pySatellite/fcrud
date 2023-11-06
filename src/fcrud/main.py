from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

class Potato(BaseModel):
    id: int
    name: str
    color: str
    mass: float

app = FastAPI()
app.include_router(CRUDRouter(schema=Potato))


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
