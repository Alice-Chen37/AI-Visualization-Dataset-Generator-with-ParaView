import json
import urllib.request

def fetch_la_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=34.05&longitude=-118.24&current_weather=true"
    
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    return {
        "temp": data["current_weather"]["temperature"],
        "wind": data["current_weather"]["windspeed"]
    }