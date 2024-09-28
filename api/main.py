from fastapi import FastAPI
from readBQ import read_app_info

app = FastAPI()


@app.get("/app_info/{app_id}:{app_department}")
def app_info(app_id: int, app_department: str):
    try:
        return read_app_info(app_id, app_department)
    except Exception as e:
        return "You have to authenticate in your company portal"


@app.get("/get_data/{department}:{num}")
def get_data(department: str, num: int):
    return {"Department": department, "Number": num}


@app.get("/health")
def health():
    return {"Status: OK"}
