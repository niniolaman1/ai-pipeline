def check_value(name, value):
    if value is None:
        return "missing"
    if value < 0:
        return "suspect_negative"
    return "ok"

MEASUREMENTS = ["no2", "pm2_5", "pm10"]


def check_reading(reading):
    result = {"datetime": reading["datetime"]}
    for name in MEASUREMENTS:
        if name in reading:
            value = reading[name]
            result[name] = (value, check_value(name, value))
    return result

def double_check_readings(rows):
    cleaned = []
    for reading in rows:
        cleaned.append(check_reading(reading))
    return cleaned

def make_row(serial, item):
    no2_value, no2_label = item.get("no2", (None, None))
    pm2_5_value, pm2_5label = item.get("pm2_5", (None, None))
    pm10_value, pm10_label = item.get("pm10", (None, None))

    return (
        serial,
        item["datetime"],
        no2_value, no2_label,
        pm2_5_value, pm10_label,
        pm10_value, pm10_label,
    )

def clean_readings(serial, rows):
    checked = double_check_readings(rows)
    clean = []
    for item in checked:
        clean.append(make_row(serial, item))
    return clean