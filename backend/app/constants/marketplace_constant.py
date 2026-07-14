from enum import StrEnum

class Role(StrEnum):
    PENDING: str = "pending"
    PAID: str = "paid"
    SHIPPED: str = "shipped"
    DELIVERED: str = "delivered"
    CANCELLED: str = "cancelled"