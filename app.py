import os
import sys
import requests
from dotenv import load_dotenv

from db import SessionLocal
from models import WeatherSnapshot

## create the url to get the weather data for the given city 
def build_url(city: str, api_key: str) -> str:
    return (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={requests.utils.quote(city)}&units=metric&appid={api_key}"
    )

## fetch the weather data by using the url created by the build_url
def fetch_weather(city: str, api_key: str) -> dict:
    url = build_url(city, api_key)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

## save the weather data into the database
def save_snapshot(data: dict) -> int:
    session = SessionLocal()
    try:
        snap = WeatherSnapshot(
            city=data.get("name") or "",
            country=(data.get("sys") or {}).get("country"),
            lat=(data.get("coord") or {}).get("lat"),
            lon=(data.get("coord") or {}).get("lon"),
            temp_c=(data.get("main") or {}).get("temp"),
            feels_like_c=(data.get("main") or {}).get("feels_like"),
            humidity=(data.get("main") or {}).get("humidity"),
            weather_main=((data.get("weather") or [{}])[0]).get("main"),
            weather_desc=((data.get("weather") or [{}])[0]).get("description"),
            observed_unix=data.get("dt"),
        )
        session.add(snap)
        session.commit()
        session.refresh(snap)
        return snap.id
    except:
        session.rollback()
        raise
    finally:
        session.close()

## main fuction to load the .env file and then load the data 
def main():
    load_dotenv()

    api_key = os.getenv("NEXT_PUBLIC_WEATHER_API_KEY")
    if not api_key:
        raise SystemExit("Missing env var NEXT_PUBLIC_WEATHER_API_KEY. Create a .env file first.")

    city = "New York"
    if len(sys.argv) >= 2:
        city = " ".join(sys.argv[1:]).strip()

    data = fetch_weather(city, api_key)
    row_id = save_snapshot(data)
    print(f"Saved weather snapshot id={row_id} for city='{data.get('name')}'")

if __name__ == "__main__":
    main()