from fastapi import FastAPI
from readBQ import read_app_info


app = FastAPI()


@app.get("/app_info/{app_id}-{app_department}")
def app_info(app_id: int, app_department: str):
    return read_app_info(app_id, app_department)


@app.get("/health")
def health():
    return {"Status: OK"}
