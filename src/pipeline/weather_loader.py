import os
import psycopg2

def insert_weather(rows):
    if not rows:
        return

    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    cur = conn.cursor()

    values = [
        (
            row["recorded_at"],
            row["forecasted_for"],
            row["latitude"],
            row["longitude"],
            row.get("temperature_c"),
            row.get("wind_speed_mps"),
            row.get("humidity_pct"),
            row.get("pressure_hpa"),
            row.get("cloudiness_pct"),
            row.get("dewpoint_c"),
            row.get("precipitation_mm"),
            row.get("symbol"),
        )
        for row in rows
    ]

    from psycopg2.extras import execute_values
    execute_values(
        cur,
        """
        INSERT INTO weather_forecasts
            (recorded_at, forecasted_for, latitude, longitude,
            temperature_c, wind_speed_mps, humidity_pct, pressure_hpa,
            cloudiness_pct, dewpoint_c, precipitation_mm, symbol)
        VALUES %s
        ON CONFLICT (latitude, longitude, forecasted_for) DO UPDATE SET
            recorded_at = EXCLUDED.recorded_at,
            temperature_c = EXCLUDED.temperature_c,
            wind_speed_mps = EXCLUDED.wind_speed_mps,
            humidity_pct = EXCLUDED.humidity_pct,
            pressure_hpa = EXCLUDED.pressure_hpa,
            cloudiness_pct = EXCLUDED.cloudiness_pct,
            dewpoint_c = EXCLUDED.dewpoint_c,
            precipitation_mm = EXCLUDED.precipitation_mm,
            symbol = EXCLUDED.symbol
        """,
        values,
    )

    conn.commit()
    cur.close()
    conn.close()