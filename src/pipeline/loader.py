import psycopg2
from psycopg2.extras import execute_values
import os

def insert_trip_updates(clean):
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    cursor = conn.cursor()

    rows_as_tuples = []
    for row in clean:
        row_tuple = (
            row["trip_id"],
            row["route_id"],
            row["direction_id"],
            row["trip_schedule_relationship"],
            row["stop_id"],
            row["stop_sequence"],
            row["stop_schedule_relationship"],
            row["arrival_delay_seconds"],
            row["departure_delay_seconds"],
            row["vehicle_id"],
            row["recorded_at"],
        )
        rows_as_tuples.append(row_tuple)


    execute_values(
        cursor,
        "INSERT INTO trip_updates (trip_id, route_id, direction_id, trip_schedule_relationship, stop_id, stop_sequence, stop_schedule_relationship, arrival_delay_seconds, departure_delay_seconds, vehicle_id, recorded_at) VALUES %s ON CONFLICT (trip_id, stop_id, recorded_at) DO NOTHING",
        rows_as_tuples,

    )

    conn.commit()
    cursor.close()

    conn.close()