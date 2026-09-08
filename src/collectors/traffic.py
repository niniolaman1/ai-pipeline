import requests
from dotenv import load_dotenv
import os
from pipeline.traffic_cleaner import clean_traffic
from pipeline.traffic_loader import insert_traffic
import time



load_dotenv()

locations = [
    {"name": "City Centre", "coordinates": (53.3498, -6.2603)},   # city centre
    {"name": "Airport", "coordinates": (53.4264, -6.2499)},   # airport
    {"name": "Red Cow", "coordinates":(53.3020, -6.3743)},   # Red Cow / M50-N7
    {"name": "Dun Laoghaire", "coordinates": (53.2932, -6.1343)},   # Dun Laoghaire
]


def fetch_traffic(lat, long):
    api_key = os.environ["TOMTOM_API_KEY"]
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {"key": api_key, "point": f"{lat},{long}"}


    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"fetch failed as {e}")
        return None

    if response.status_code != 200:
        print(f"fetch failed as {response.status_code}")
        return None

    try:
        feed = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"invalid JSON syntax: {e}")
        return None

    return feed

def main():
    while True:
        print("cycle starting")
        rows = []
        for loc in locations:
            raw = fetch_traffic(loc["coordinates"][0], loc["coordinates"][1])
            if raw is None:
                continue
            row = clean_traffic(loc["name"], raw)
            if row is not None:
                rows.append(row)
        insert_traffic(rows)

        time.sleep(300)





if __name__ == "__main__":
    main()




