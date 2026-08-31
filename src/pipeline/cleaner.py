from datetime import datetime, timezone

DELAY_LOWER_BOUND = -600
HOUR = 3600
DST_TOLERANCE = 120  # seconds — how close to a clean hour-multiple counts as a likely artifact

def _is_likely_dst_artifact(delay):
    remainder = abs(delay) % HOUR
    distance_to_nearest_hour_mark = min(remainder, HOUR - remainder)
    return distance_to_nearest_hour_mark <= DST_TOLERANCE

def clean_trip_updates(feed):
    clean = []

    for entity in feed.entity:
        trip = entity.trip_update.trip

        trip_id = trip.trip_id
        route_id = trip.route_id if trip.HasField("route_id") else None
        direction_id = trip.direction_id if trip.HasField("direction_id") else None
        trip_schedule_relationship = trip.schedule_relationship

        vehicle_id = entity.trip_update.vehicle.id if entity.trip_update.HasField("vehicle") else None

        recorded = entity.trip_update.timestamp
        recorded_at = datetime.fromtimestamp(recorded, tz=timezone.utc)

        for stu in entity.trip_update.stop_time_update:
            arrival_delay = stu.arrival.delay if stu.HasField("arrival") else None
            departure_delay = stu.departure.delay if stu.HasField("departure") else None

            if arrival_delay is not None and arrival_delay < DELAY_LOWER_BOUND:
                if _is_likely_dst_artifact(arrival_delay):
                    print(f"omo na possible DST/timezone artifact: trip na {trip_id}, arrival delay na {arrival_delay}")
                else:
                    print(f"oga this bus dey too early oo. the trip_id na {trip_id}, and e don delay by {arrival_delay}")
                continue

            if departure_delay is not None and departure_delay < DELAY_LOWER_BOUND:
                if _is_likely_dst_artifact(departure_delay):
                    print(f"omo na possible DST/timezone artifact: trip na {trip_id}, departure delay na {departure_delay}")
                else:
                    print(f"oga this bus dey too early oo. the trip_id na {trip_id}, and e don delay by {departure_delay}")
                continue

            stop_id = stu.stop_id if stu.HasField("stop_id") else None
            stop_sequence = stu.stop_sequence if stu.HasField("stop_sequence") else None
            stop_schedule_relationship = stu.schedule_relationship if stu.HasField("schedule_relationship") else None

            row = {
                "trip_id": trip_id,
                "route_id": route_id,
                "direction_id": direction_id,
                "trip_schedule_relationship": trip_schedule_relationship,
                "stop_id": stop_id,
                "stop_sequence": stop_sequence,
                "stop_schedule_relationship": stop_schedule_relationship,
                "arrival_delay_seconds": arrival_delay,
                "departure_delay_seconds": departure_delay,
                "vehicle_id": vehicle_id,
                "recorded_at": recorded_at,
            }
            clean.append(row)

    return clean








