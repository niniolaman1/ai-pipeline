from fastapi import FastAPI, HTTPException
from collectors.air_sensors import SENSORS
from api.gtfs import ROUTES, AGENCIES, STOPS
from dotenv import load_dotenv
from api.db import get_connection

load_dotenv()

app = FastAPI()

@app.get("/air/sensors")
def all_sensors():
    sensors = []
    for serial, place in SENSORS.items():
        sensors.append({"serial": serial, "place": place})

    return {"count": len(sensors), "sensors": sensors}

@app.get("/air/sensors/{serial}")
def get_sensor(serial):
    if serial not in SENSORS:
        raise HTTPException(status_code=404, detail="not a sensor")
    return {"serial": serial, "place": SENSORS[serial]}

@app.get("/air/sensors/{serial}/recent")
def recent_readings(serial, limit: int = 5):
    if serial not in SENSORS:
        raise HTTPException(status_code=404, detail="not a sensor")

    if 1 <= limit <= 100:
        pass
    else:
        raise HTTPException(status_code=422, detail="out of limit, limit needs to be between 1 - 100")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT recorded_at, no2, pm2_5, pm10
            FROM air_quality_readings
            WHERE serial_number = %s
            ORDER BY recorded_at DESC
            LIMIT %s
            """,
            (serial, limit),
        )
        data = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    readings = []
    for recorded, no2, pm2_5, pm10 in data:
        readings.append({"recorded_at":recorded, "no2": no2, "pm2_5": pm2_5, "pm10": pm10})

    return {
        "serial": serial,
        "place": SENSORS[serial],
        "readings": readings,
    }

@app.get("/air/latest")
def get_the_most_recent_sensors():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT DISTINCT ON (serial_number) serial_number,
                recorded_at, no2, pm2_5, pm10
            FROM air_quality_readings
            ORDER BY serial_number, recorded_at DESC
            """,
        )
        data = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    readings = []
    for serial, recorded, no2, pm2_5, pm10 in data:
        readings.append({"serial": serial, "place": SENSORS.get(serial, "unknown"), "recorded_at": recorded, "no2": no2, "pm2_5": pm2_5, "pm10": pm10})

    return {
        "count": len(readings),
        "readings": readings,
    }

@app.get("/bus/routes/{number}")
def get_bus_no(number):
    number = number.upper()

    if number not in ROUTES:
        raise HTTPException(status_code=404, detail="not a bus route")

    routes = ROUTES[number]
    count = len(routes)

    return {"number": number, "count": count, "routes": routes}

@app.get("/bus/routes/{number}/stops/{stop_number}")
def gets_bus_and_and_stop(number, stop_number):
    number = number.upper()

    if number not in ROUTES:
        raise HTTPException(status_code=404, detail="not a bus route")
    if stop_number not in STOPS:
        raise HTTPException(status_code=404, detail="not a stop")

    stop = STOPS[stop_number][0]["stop_name"]

    stop_ids = []
    for i in STOPS[stop_number]:
        stop_ids.append(i["stop_id"])

    conn = get_connection()
    cur = conn.cursor()

    try:
        routes = []
        for row in ROUTES[number]:
            route_id_1 = row["route_id"]
            route_id_2 = route_id_1.replace("_", " ")

            cur.execute(
                """
                SELECT recorded_at, arrival_delay_seconds, departure_delay_seconds, stop_schedule_relationship
                FROM trip_updates
                WHERE (route_id = %s OR route_id = %s)
                AND stop_id = ANY(%s)
                ORDER BY recorded_at DESC, stop_schedule_relationship
                LIMIT 1
                """,
                (route_id_1, route_id_2, stop_ids,),
            )

            data = cur.fetchone()

            if not data:
                continue

            as_of, arrival_delay, departure_delay, status = data
            if status == "0":
                status = "scheduled"
            elif status == "1":
                status = "skipped"
            else:
                status = "no data"

            latest = {
                "as_of": as_of,
                "status": status,
                "arrival_delay": arrival_delay,
                "departure_delay": departure_delay,
                }

            routes.append({"company":row["company"],
                        "route": row["route_long_name"], "latest": latest},)

    finally:
        cur.close()
        conn.close()

    if not routes:
        raise HTTPException(status_code=404, detail="stop number not in bus route")


    output = {
        "number": number,
        "stop": stop,
        "stop_number": stop_number,
        "routes": routes,
        }

    return output