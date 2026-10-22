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

