# OpenWeather API -> SQLite (Python)

This repo will:
1) Fetching data from an OpenWeatherMap REST API
2) Saving the fetched data into SQLite
3) Managing database schema using Alembic migrations

## Project Structure
 `app.py` - Fetches weather data from OpenWeatherMap and saves it to the database
 `models.py` - SQLAlchemy ORM models (database schema)
 `db.py` - Database connection/session setup
 `migrations/` - Alembic migrations (schema setup)
 `requirements.txt` - Python dependencies

## Requirements
 Python 3.9+ (any Python 3.x should work)
 An OpenWeatherMap API key
## Setup

### 1 Create and activate a virtual environment

in bash

python3 -m venv weather
source weather/bin/activate
pip install -r requirements.txt


### 2 Database Setup (Migrations)

Run Alembic migrations (creates data.db and tables)

in bash

alembic upgrade head

This will create a SQLite database file named data.db in the project root and create the table weather_snapshots.

### 3 Run the Program

Fetch weather data and store it in the database

run 

python app.py "New York"