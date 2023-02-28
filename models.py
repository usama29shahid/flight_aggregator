from sqlalchemy import Column, Integer, String, Date, Time
from database import Base

class Mmt_flights(Base):
    __tablename__ = 'mmt'

    id = Column(Integer, primary_key=True, index=True)
    flight_date = Column(String)
    airline = Column(String)
    airline_number = Column(String)
    departure_time = Column(String)
    origin = Column(String)
    flight_duration = Column(String)
    stops = Column(String)
    arrival_time = Column(String)
    destination = Column(String)
    fare = Column(String)
    other = Column(String)
    currency = Column(String)
    amount = Column(Integer)
    capture_timestamp_epoch = Column(Integer)
    capture_date = Column(Date)
    capture_timestamp = Column(Time)