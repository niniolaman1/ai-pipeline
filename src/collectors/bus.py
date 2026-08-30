import os
import requests
from dotenv import load_dotenv
import certifi

def fetch_gtfs_rt():
    load_dotenv()
    api_key = os.environ["NTA_PRIMARY_KEY"]
    url = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
    headers = {"x-api-key": api_key}


    response = requests.get(url=url, headers=headers, verify=certifi.where())

    if response.status_code == 200:
        from google.transit import gtfs_realtime_pb2
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    else:
        print(response.status_code)
        return None

def main():
    feed = fetch_gtfs_rt()
    if feed:
        print(len(feed.entity))
    else:
        print("omo the fetch failed oo")


if __name__ == "__main__":
    main()
