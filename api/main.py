from fastapi import FastAPI
from readBQ import read_app_info

app = FastAPI()


@app.get("/app_info/{app_id}:{app_department}")
def app_info(app_id: int, app_department: str):
    try:
        return read_app_info(app_id, app_department)
    except Exception as e:
        return "You have to authenticate in your company portal"


@app.get("/get_data/{action_id}:{user_email}")
def get_data(action_id: str, user_email: int):
    return {"Action Id": action_id, "Email": user_email}


@app.get("/health")
def health():
    return {"Status: OK"}
