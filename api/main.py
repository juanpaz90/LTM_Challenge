from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from readBQ import read_app_info


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/app_info/{app_id}-{app_department}")
def app_info(app_id: int, app_department: str):
    return read_app_info(app_id, app_department)


@app.get("/items/{item_id}-{test}")
def read_item(item_id: int, test: str):
    return {"item_id": item_id, "test": test}


@app.get("/health")
def health():
    return {"Status: OK"}
