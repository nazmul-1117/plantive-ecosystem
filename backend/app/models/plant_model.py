from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

class Plants(SQLModel, table=True):
    __tablename__="plants"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True
        ),
        default_factory=uuid.uuid4
    )
    
    name: str
    description: str
    type: str
    price: float
    stock: int

    # created and updated at both are same
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        default_factory=datetime.now
    )