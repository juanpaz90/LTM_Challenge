from google.cloud import bigquery


def read_app_info(app_id, app_department):
    client = bigquery.Client()
    query_job = client.query(f"""
        SELECT *
        FROM `global-app-project.enterprise_app_dataset.latest_table`
        WHERE app_id = '{app_id}'
        AND app_department = {app_department}
        """)
    results = query_job.result()
    return results
