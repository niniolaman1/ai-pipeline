import os
import requests
from dotenv import load_dotenv
import certifi
import time
from pipeline.cleaner import clean_trip_updates
from pipeline.loader import insert_trip_updates

def fetch_gtfs_rt():
    load_dotenv()
    api_key = os.environ["NTA_PRIMARY_KEY"]
    url = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
    headers = {"x-api-key": api_key}


    try:
        response = requests.get(url=url, headers=headers, verify=certifi.where())
    except requests.exceptions.RequestException as e:
        print(f"fetch failed with an exception: {e}")
        return None

    if response.status_code == 200:
        from google.transit import gtfs_realtime_pb2
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    else:
        print(response.status_code)
        return None

def main():
    while True:
        feed = fetch_gtfs_rt()
        if feed:
            clean_rows = clean_trip_updates(feed)
            insert_trip_updates(clean_rows)
            print(f"inserted (or skipped duplicates for) {len(clean_rows)} rows")
        else:
            print("fetch failed")

        time.sleep(300)


if __name__ == "__main__":
    main()
