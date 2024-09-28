import pandas as pd
import pandas_gbq
import datetime


def current_date() -> datetime:
    return datetime.date.today()


def create_dict(app_id, app_department, action_id, department_id, user_email) -> dict:
    date = current_date()
    data = {
        "app_id": app_id,
        "app_department": app_department,
        "joined_project_list": action_id,
        "department_id": department_id,
        "user_email": user_email,
        "date": date,
    }
    return data


def modify_df(dict_data):
    data_frame = pd.DataFrame(dict_data, index=[0])
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    return data_frame


def store_user_app_data(app_id, app_department, action_id, department_id, user_email):
    table_id = 'global-app-project.enterprise_app_dataset.latest_table'
    dict_data = create_dict(app_id, app_department, action_id, department_id, user_email)
    data_frame = modify_df(dict_data)
    try:
        pandas_gbq.to_gbq(data_frame, table_id, if_exists='append')
        print(f"SUCCESS - Data transferred to {table_id}")
    except Exception as e:
        print(f"ERROR: {e}")