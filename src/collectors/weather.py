import requests
from xml.etree import ElementTree as ET

def fetch_weather():
    url = "http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast?lat=53.3498;long=-6.2603"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"fetch failed as {e}")
        return None

    if response.status_code != 200:
        print(f"fetch failed as {response.status_code}")

    try:
        root = ET.fromstring(response.text)
        print(response.status_code)
    except ET.ParseError as e:
        print(f"parse failed as {e}")
        return None

    return root


