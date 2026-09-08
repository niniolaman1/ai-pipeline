import datetime

def clean_traffic(location, data):
    if data.get("flowSegmentData") is not None:
        data = data["flowSegmentData"]
    else:
        return None

    fetched_at = datetime.datetime.now()
    confidence = data["confidence"]
    current_speed = data["currentSpeed"]
    current_travel_time = data["currentTravelTime"]
    free_flow_speed = data["freeFlowSpeed"]
    free_flow_travel_time = data["freeFlowTravelTime"]
    road_closure = data["roadClosure"]
    frc = data["frc"]

    if confidence > 0.5:
        clean = {
            "location": location,
            "fetched_at": fetched_at,
            "confidence": confidence,
            "current_speed": current_speed,
            "current_travel_time": current_travel_time,
            "free_flow_speed": free_flow_speed,
            "free_flow_travel_time": free_flow_travel_time,
            "road_closure": road_closure,
            "frc": frc,
        }

    else:
        print(f"confidence is too low : {confidence} at {location}")
        return None



    return clean



