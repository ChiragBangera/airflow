import json
import requests
import pandas as pd
from pathlib import Path
import datetime as dt
from opensky_api import OpenSkyApi
from zoneinfo import ZoneInfo


from airflow import DAG
from airflow.operators.python import PythonOperator


def _get_city_bike_data(city_name: str = "chartered-bike-prayagraj"):
    url = f"https://api.citybik.es/v2/networks/{city_name}"
    try:
        res = requests.get(url)
        print(res.status_code)
        json_result = res.json()

    except requests.exceptions.HTTPError as e:
        return e

    except requests.exceptions.JSONDecodeError as e:
        return e

    except requests.exceptions.RequestException as e:
        print(e)
        return e

    dump_folder = Path(f"/home/chirag/airflow/appfiles/tmp/{city_name}")

    preprocess_status_log_file = Path(
        "/home/chirag/airflow/appfiles/tmp/pre_process_status.json"
    )

    if not dump_folder.is_dir():
        dump_folder.mkdir(parents=True, exist_ok=True)

    file_name = (
        f"events_{dt.datetime.now().astimezone(ZoneInfo("Asia/Kolkata")).date()}.json"
    )
    dump_file_loc = dump_folder / file_name

    if not dump_file_loc.is_file():
        with open(dump_file_loc, "w") as file:
            json.dump(json_result, file, indent=4)

        log_identifier = str(f"{city_name}_{file_name}")

        try:
            with open(preprocess_status_log_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data[log_identifier] = {
            "pre_process_status": False,
            "file_loc": str(dump_file_loc),
            "dump_timestamp": str(
                dt.datetime.now().astimezone(ZoneInfo("Asia/Kolkata"))
            ),
            "city_name": str(city_name),
            "file_name": str(file_name),
        }

        with open(preprocess_status_log_file, "w") as file:
            json.dump(data, file, indent=4)


def parse_json_bike_data(json_data):
    main = json_data["network"]
    stations = json_data["network"]["stations"]
    print(len(stations))


res = _get_city_bike_data()
print(dt.date.today())
