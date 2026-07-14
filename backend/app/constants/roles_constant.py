from enum import StrEnum

class RoleConstant(StrEnum):
    ADMIN: str = "admin"
    USER: str = "user"
    MODERATOR: str = "moderator"