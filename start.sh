#!/bin/zsh

if [ ! -d "src" ]; then
    echo "Error: run this script frm the ai-pipeline root directory"
    exit 1
fi

if [ ! -d "logs" ]; then
    mkdir logs
    echo "Created logs/directory"
else
    echo "logs/directory already exixts"
fi

echo "Starting CityPulse collectors...."



python src/collectors/bus.py > logs/bus.log 2>&1 &
BUS_PID=$!
echo "Bus collector started - PID: $BUS_PID"

python src/collectors/weather.py > logs/weather.log 2>&1 &
WEATHER_PID=$!
echo "Weather collector started - PID: $WEATHER_PID"

python src/collectors/air_quality.py > logs/air_quality.log 2>&1 &
AIR_PID=$!
echo "Air quality collector started - PID: $AIR_PID"

python src/collectors/traffic.py > logs/traffic.log 2>&1 &
TRAFFIC_PID=$!
echo "Traffic collector started - PID: $TRAFFIC_PID"


echo "bus: $BUS_PID" > pids.txt
echo "weather: $WEATHER_PID" >> pids.txt
echo "air_quality: $AIR_PID" >> pids.txt
echo "traffic: $TRAFFIC_PID" >> pids.txt

echo "ALL collectors running. PIDs saved to pids.txt"
