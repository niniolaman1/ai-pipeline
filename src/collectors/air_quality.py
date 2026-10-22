import os
import requests
from dotenv import load_dotenv
import certifi
import time
from collectors.air_sensors import SENSORS

load_dotenv()

URL = "https://data.smartdublin.ie/sonitus-api/api/data"

def fetch_readings(serial, start, end):
    body = {
        "username": os.environ["SONITUS_USER"],
        "password": os.environ["SONITUS_PASSWORD"],
        "monitor": serial,
        "start": start,
        "end": end,
    }

    try:
        response = requests.post(URL, json=body, verify=certifi.where(), timeout=30)
    except requests.exceptions.RequestsExceptions as e:
        print(f"{serial}: requests failed ({type(e).__name__})")
        return None

    try:
        data = response.json()
    except ValueError:
        print(f"{serial}: reply was not JSON (status {response.status_code})")
        return None

    if isinstance(data, dict) and "error" in data:
        print(f"{serial}: service said: {data['error']}")
        return None

    return data


def fetch_all(hours=24):
    now = int(time.time())
    start = now - hours * 3600

    results = {}
    for serial, place in SENSORS.items():
        rows = fetch_readings(serial, start, now)
        if rows is None:
            print(f"{place}: no usable reply, skipping")
        else:
            results[serial] = rows
        time.sleep(0.3)

    return results