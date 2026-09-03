def clean_weather(root):

    harmonie = root.find(".//model[@name='harmonie']")
    termin = harmonie.get("termin")
    harmonie_to = harmonie.get("to")
    harmonie_from = harmonie.get("from")

    merged = {}
    for time in root.find("product").findall("time"):
        time_to = time.get("to")
        location = time.find("location")
        latitude = location.get("latitude")
        longitude = location.get("longitude")

        if time_to < harmonie_from or time_to > harmonie_to:
            continue

        row = merged.setdefault(time_to, {"recorded_at": termin, "forecasted_for": time_to, "latitude": latitude, "longitude": longitude})

        temp = location.find("temperature")
        if temp is not None:
            row["temperature_c"] = float(temp.get("value"))
            row["wind_speed_mps"] = float(location.find("windSpeed").get("mps"))
            row["humidity_pct"] = float(location.find("humidity").get("value"))
            row["pressure_hpa"] = float(location.find("pressure").get("value"))
            row["cloudiness_pct"] = float(location.find("cloudiness").get("percent"))
            row["dewpoint_c"] = float(location.find("dewpointTemperature").get("value"))

        precip = location.find("precipitation")
        if precip is not None:
            row["precipitation_mm"] = float(precip.get("value"))
            symbol = location.find("symbol")
            row["symbol"] = symbol.get("id") if symbol is not None else None


    return list(merged.values())





