import json
import requests
import pandas as pd
from pathlib import Path
import datetime as dt
from opensky_api import OpenSkyApi

from airflow import DAG
from airflow.operators.python import PythonOperator


def get_city_bike_data(city_name: str = "chartered-bike-prayagraj"):
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

    return json_result


def parse_json_bike_data(json_data):
    main = json_data["network"]
    stations = json_data["network"]["stations"]
    print(len(stations))


res = parse_json_bike_data(get_city_bike_data())

# res = requests.get("https://api.citybik.es/v2/networks/chartered-bike-prayagr")
# try:
#     json_result = res.json()
# except requests.exceptions.JSONDecodeError as e:
#     print(e)


# rocket launch
# def _get_launch_data():
#     url = "https://ll.thespacedevs.com/2.0.0/launch/upcoming"
#     tmp = Path("appfiles/tmp/launches.json")
#     data = {}
#     if not tmp.is_file():
#         try:
#             res = requests.get(url)
#             res.raise_for_status()
#             data = res.json()
#         except requests.exceptions.RequestException as e:
#             print(e)
#         Path("appfiles/tmp").mkdir(parents=True, exist_ok=True)
#         with open(tmp, "w") as json_file:
#             json.dump(data, json_file, indent=4)


# def _get_pictures():
#     tmp = Path("appfiles/tmp/images")
#     if not tmp.is_dir():
#         tmp.mkdir(parents=True, exist_ok=True)

#         # Download all pictures in the launches.json
#         with open("appfiles/tmp/launches.json") as f:
#             launches = json.load(f)
#             image_urls = [launch["image"] for launch in launches["results"]]
#         for image in image_urls:
#             image_name = image.split("/")[-1]
#             target_path = tmp / image_name
#             try:
#                 res = requests.get(image)
#                 with open(target_path, "wb") as f:
#                     f.write(res.content)
#             except requests.exceptions.MissingSchema:
#                 print(f"{image} is not valid url")
#             except requests.exceptions.ConnectionError:
#                 print(f"Could not connect for {image}")


# data = _get_launch_data()
# _get_pictures()

# api = OpenSkyApi()

# departures = api.get_departures_by_airport("VOBL", 1731349800, 1731436200)
# for drparture in departures:
#     print(drparture, "\n--------,")
