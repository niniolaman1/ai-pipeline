from fastapi import FastAPI, HTTPException
from collectors.air_sensors import SENSORS
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