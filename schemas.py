from pydantic import BaseModel
from datetime import date

class Client(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    registration_date: date