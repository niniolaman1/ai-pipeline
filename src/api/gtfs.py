import csv

AGENCIES = {}
with open("src/data/gtfs/agency.txt", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        AGENCIES[row["agency_id"]] = row["agency_name"]


print(AGENCIES)

ROUTES = {}
with open("src/data/gtfs/routes.txt", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        bus_no = row["route_short_name"]
        if bus_no not in ROUTES.keys():
            ROUTES[bus_no] = []
        ROUTES[bus_no].append({"route_id":row["route_id"], "agency_id":row["agency_id"],"company":AGENCIES[row["agency_id"]], "route_long_name":row["route_long_name"]})

print(ROUTES)