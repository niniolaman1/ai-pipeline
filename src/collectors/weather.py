import requests
from xml.etree import ElementTree as ET
from pipeline.weather_cleaner import clean_weather
from pipeline.weather_loader import insert_weather
import time
from dotenv import load_dotenv

load_dotenv()

locations = [
    (53.3498, -6.2603),   # city centre
    (53.4264, -6.2499),   # airport
    (53.3020, -6.3743),   # Red Cow / M50-N7
    (53.2932, -6.1343),   # Dun Laoghaire
]

def fetch_weather(lat, long):
    url = f"http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast?lat={lat};long={long}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"fetch failed as {e}")
        return None

    if response.status_code != 200:
        print(f"fetch failed as {response.status_code}")
        return None

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"parse failed as {e}")
        return None

    return root

def main():
    while True:
        print("cycle starting")
        all_rows = []
        for lat, long in locations:
            root = fetch_weather(lat, long)
            if root is None:
                continue
            rows = clean_weather(root)
            all_rows.extend(rows)

        insert_weather(all_rows)
        time.sleep(300)




if __name__ == "__main__":
    main()




