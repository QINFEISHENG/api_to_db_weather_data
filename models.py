## import all the packages 

## allthe ORM models will inherit from this DeclarativeBase base class
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime
from datetime import datetime

## all the models will be defined here , by using the DeclarativeBase
class Base(DeclarativeBase):
    pass

class WeatherSnapshot(Base):
    ## create a table named weather_snapshots in the database.
    __tablename__ = "weather_snapshots"
    ## set the id  as the primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ## set for the rest of the data 
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    country: Mapped[str] = mapped_column(String(10), nullable=True)

    lat: Mapped[float] = mapped_column(Float, nullable=True)
    lon: Mapped[float] = mapped_column(Float, nullable=True)

    temp_c: Mapped[float] = mapped_column(Float, nullable=True)
    feels_like_c: Mapped[float] = mapped_column(Float, nullable=True)
    humidity: Mapped[int] = mapped_column(Integer, nullable=True)

    weather_main: Mapped[str] = mapped_column(String(50), nullable=True)
    weather_desc: Mapped[str] = mapped_column(String(120), nullable=True)


    observed_unix: Mapped[int] = mapped_column(Integer, nullable=True)
    fetched_at_utc: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)