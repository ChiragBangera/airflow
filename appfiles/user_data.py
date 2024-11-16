import datetime as dt
from pathlib import Path
import json
import requests
from zoneinfo import ZoneInfo

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


dag = DAG(
    dag_id="bike_data_unscheduled",
    start_date=dt.datetime(2024, 11, 1),
    schedule_interval=None,
)


def _get_city_bike_data(city_name: str = "chartered-bike-prayagraj"):
    url = f"https://api.citybik.es/v2/networks/{city_name}"

    dump_folder = Path(f"/home/chirag/airflow/appfiles/tmp/{city_name}")

    preprocess_status_file = Path(
        "/home/chirag/airflow/appfiles/tmp/pre_process_status.json"
    )

    file_name = (
        f"events_{dt.datetime.now().astimezone(ZoneInfo("Asia/Kolkata")).date()}.json"
    )

    log_identifier = str(f"{city_name}_{file_name}")

    dump_file_loc = dump_folder / file_name

    try:
        with open(preprocess_status_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    try:
        res = requests.get(url)
        json_result = res.json()

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.JSONDecodeError,
        requests.exceptions.RequestException,
    ) as e:
        return e

    if not dump_folder.is_dir():
        dump_folder.mkdir(parents=True, exist_ok=True)

    if not dump_file_loc.is_file():
        with open(dump_file_loc, "w") as file:
            json.dump(json_result, file, indent=4)

        data[log_identifier] = {
            "pre_process_status": False,
            "file_loc": str(dump_file_loc),
            "dump_timestamp": str(
                dt.datetime.now().astimezone(ZoneInfo("Asia/Kolkata"))
            ),
            "city_name": str(city_name),
            "file_name": str(file_name),
        }

        with open(preprocess_status_file, "w") as file:
            json.dump(data, file, indent=4)


fetch_bike_data = PythonOperator(
    task_id="fetch_bike_data", python_callable=_get_city_bike_data, dag=dag
)
