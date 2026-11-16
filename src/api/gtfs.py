import csv

AGENCIES = {}
with open("src/data/gtfs/agency.txt", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        AGENCIES[row["agency_id"]] = row["agency_name"]




ROUTES = {}
with open("src/data/gtfs/routes.txt", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        bus_no = row["route_short_name"].upper()
        if bus_no not in ROUTES.keys():
            ROUTES[bus_no] = []
        ROUTES[bus_no].append({"route_id":row["route_id"], "agency_id":row["agency_id"],"company":AGENCIES[row["agency_id"]], "route_long_name":row["route_long_name"]})



STOPS = {}
with open("src/data/gtfs/stops.txt", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        stop_code = row["stop_code"]
        if stop_code not in STOPS:
            STOPS[stop_code] = []
        STOPS[stop_code].append({"stop_id": row["stop_id"], "stop_name": row["stop_name"]})

