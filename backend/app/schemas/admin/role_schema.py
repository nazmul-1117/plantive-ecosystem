
# schema/admin/role_schema.py -> admin

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

# Request Schema
class AdminAssignRoleRequest(BaseModel):
    role_uid: UUID



# Response Schema
class AdminUserRolesResponse(BaseModel):
    role_uid: UUID
    name: str
    description: str | None = None
    is_active: bool

class AdminRoleReadResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    role_uid: UUID
    name: str
    description: str
    is_active: bool
    
    # Audit
    created_at: datetime
    updated_at: datetime




# Data Schema