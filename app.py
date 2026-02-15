# load all the required packages
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
    # build the url by using the city name and the api key
    url = build_url(city, api_key)
    ## MUST SET a timeout to make sure the api is actually responding
    ## it should return within 30 , 
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    ## return the data in the json format .
    return r.json()

## save the weather data into the database
def save_snapshot(data: dict) -> int:
    ## create a new session to talk to the database 
    session = SessionLocal()
    try:

        snap = WeatherSnapshot(
            ##get the city name from the data 
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
        ## must commit the session to save the data!
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
    ## load the api key into the environment
    load_dotenv()
    # assgin the api ket 
    api_key = os.getenv("NEXT_PUBLIC_WEATHER_API_KEY")
    ## handling the error when the api key is missing 
    if not api_key:
        raise SystemExit("Missing env var NEXT_PUBLIC_WEATHER_API_KEY. Create a .env file first.")
    ## set the default city to New York lol
    city = "New York"
    if len(sys.argv) >= 2:
        city = " ".join(sys.argv[1:]).strip()

    data = fetch_weather(city, api_key)
    row_id = save_snapshot(data)
    print(f"Saved weather snapshot id={row_id} for city='{data.get('name')}'")

# run the main funcion when the script is being executed.
if __name__ == "__main__":
    main()