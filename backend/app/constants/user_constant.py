from enum import StrEnum

# instead of is_active
class UserStatus(StrEnum):
    ACTIVE: str = "active"
    INACTIVE: str = "inactive"
    SUSPENDED: str = "suspended"
    BANNED: str = "banned"