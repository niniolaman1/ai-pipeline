import os
import psycopg2
from psycopg2.extras import execute_values


def insert_traffic(clean):
    if not clean:
        return


    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    cur = conn.cursor()

    values = [
        (
            i["location"],
            i["fetched_at"],
            i["confidence"],
            i["current_speed"],
            i["current_travel_time"],
            i["free_flow_speed"],
            i["free_flow_travel_time"],
            i["road_closure"],
            i["frc"],
        )
        for i in clean
    ]

    try:
        execute_values(
            cur,
            """
                INSERT INTO traffic_data(
                    location, fetched_at, confidence, current_speed,
                    current_travel_time, free_flow_speed, free_flow_travel_time,
                    road_closure, frc
                )
                VALUES %s
                ON CONFLICT (location, fetched_at) DO NOTHING
            """,
            values,
        )
        conn.commit()

    except psycopg2.Error as e:
        print(f"insert failed as {e}")

    finally:
        cur.close()
        conn.close()
