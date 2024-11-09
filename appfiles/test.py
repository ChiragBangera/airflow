import json
import requests
from pathlib import Path


def _get_launch_data():
    url = "https://ll.thespacedevs.com/2.0.0/launch/upcoming"
    tmp = Path("appfiles/tmp/launches.json")
    data = {}
    if not tmp.is_file():
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException as e:
            print(e)
        Path("appfiles/tmp").mkdir(parents=True, exist_ok=True)
        with open(tmp, "w") as json_file:
            json.dump(data, json_file, indent=4)


def _get_pictures():
    tmp = Path("appfiles/tmp/images")
    if not tmp.is_dir():
        tmp.mkdir(parents=True, exist_ok=True)

        # Download all pictures in the launches.json
        with open("appfiles/tmp/launches.json") as f:
            launches = json.load(f)
            image_urls = [launch["image"] for launch in launches["results"]]
        for image in image_urls:
            image_name = image.split("/")[-1]
            target_path = tmp / image_name
            try:
                res = requests.get(image)
                with open(target_path, "wb") as f:
                    f.write(res.content)
            except requests.exceptions.MissingSchema:
                print(f"{image} is not valid url")
            except requests.exceptions.ConnectionError:
                print(f"Could not connect for {image}")


data = _get_launch_data()
_get_pictures()
