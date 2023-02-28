from pydantic import BaseModel, Field
from datetime import date

class MMT(BaseModel):
    origin: str = Field(min_length=3, max_length=3, description='Origin must be 3 length like DEL')
    destination: str = Field(min_length=3, max_length=3, description='Destination must be 3 length like DEL')
    my_date: date
