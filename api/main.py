from fastapi import FastAPI, HTTPException
from readBQ import read_app_info

app = FastAPI()


@app.get("/app_info/{app_id}:{app_department}")
def app_info(app_id: int, app_department: str):
    try:
        return read_app_info(app_id, app_department)
    except Exception as e:
        raise HTTPException(status_code=401, detail="You have to authenticate in your company portal")


@app.get("/get_data/{action_id}:{user_email}")
def get_data(action_id: int, user_email: str):
    if type(action_id) is int and type(user_email) is str:
        return {"Action Id": action_id, "Email": user_email}
    else:
        raise HTTPException(status_code=400, detail="Check the data and try again")

@app.get("/health")
def health():
    return {"Status: OK"}
