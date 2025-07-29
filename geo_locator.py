import zmq
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
assert MAPBOX_TOKEN, "Missing MAPBOX_TOKEN in environment variables"
MAPBOX_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json"
PORT = os.getenv("PORT_GEOLOCATOR", "5560")

def geocode_location(query):
    if not query.strip():
        return {"error": "Missing input"}

    url = MAPBOX_URL.format(requests.utils.quote(query))
    params = {
        "access_token": MAPBOX_TOKEN,
        "limit": 1,
        "country": "US"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        features = data.get("features")
        if not features:
            return {"error": "No result found"}

        coords = features[0]["center"]
        return {
            "lat": coords[1],
            "lon": coords[0]
        }
    except Exception as e:
        return {"error": f"Lookup failed: {str(e)}"}


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")
    print(f"[GeoLocator] MapBox microservice listening on tcp://*:{PORT}")

    try:
        while True:
            query = socket.recv_string()
            result = geocode_location(query)
            socket.send_json(result)
    except KeyboardInterrupt:
        print("[GeoLocator] Shutting down.")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
