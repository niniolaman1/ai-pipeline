import os
import psycopg2
from psycopg2.extras import execute_values


def insert_air_readings(clean):
    if not clean:
        return 0

    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    cur = conn.cursor()

    try:
        inserted = execute_values(
            cur,
            """
            INSERT INTO air_quality_readings
                (serial_number, recorded_at,
                 no2, no2_label, pm2_5, pm2_5_label, pm10, pm10_label)
            VALUES %s
            ON CONFLICT (serial_number, recorded_at) DO NOTHING
            RETURNING serial_number
            """,
            clean,
            fetch=True,
        )
        conn.commit()
        return len(inserted)

    except psycopg2.Error as e:
        conn.rollback()
        print(f"air insert failed: {e}")
        return None

    finally:
        cur.close()
        conn.close()