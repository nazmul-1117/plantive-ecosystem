from pydantic import BaseModel
from datetime import datetime
import uuid

# schemas/user.py

# UserCreate
# UserUpdate
# UserRead
# UserLogin

class Plant(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    type: str
    price: float
    stock: int
    created_at: datetime
    updated_at: datetime

class PlantCreate(BaseModel):
    name: str
    description: str
    type: str
    price: float
    stock: int

class PlantUpdate(BaseModel):
    price: float
    stock: int

