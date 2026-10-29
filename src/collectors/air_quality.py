import os
import requests
from dotenv import load_dotenv
import certifi
import time
from collectors.air_sensors import SENSORS
from pipeline.air_cleaner import clean_readings
from pipeline.air_loader import insert_air_readings

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


def main():
    while True:
        print("cycle starting")
        now = int(time.time())
        start = now - 6 * 3600

        ok = 0
        failed = []
        total_new = 0

        for serial, place in SENSORS.items():
            rows = fetch_readings(serial, start, now)
            if rows is None:
                failed.append(place)
                continue

            try:
                clean = clean_readings(serial, rows)
            except (KeyError, TypeError) as e:
                print(f"{place}: could not clean readings ({type(e).__name__})")
                failed.append(place)
                continue

            new = insert_air_readings(clean)
            if new is None:
                failed.append(place)
            else:
                ok += 1
                total_new += new
                print(f"{place}: fetched {len(rows)}, new {new}")

            time.sleep(0.3)

        print(f"cycle done: {ok} ok, {len(failed)} failed {failed}, {total_new} new rows")
        time.sleep(300)


if __name__ == "__main__":
    main()