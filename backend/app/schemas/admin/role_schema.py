
# schema/admin/role_schema.py -> admin

from uuid import UUID
from pydantic import BaseModel

# Request Schema
class AdminAssignRoleRequest(BaseModel):
    role_uid: UUID



# Response Schema
class AdminUserRolesResponse(BaseModel):
    role_uid: UUID
    name: str
    description: str | None = None
    is_active: bool



# Data Schema