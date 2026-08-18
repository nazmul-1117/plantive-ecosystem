
# app/schemas/admin/user_role_schema.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class AdminAssignUserRolesRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    role_uids: list[UUID] = Field(
        min_length=1,
        max_length=20,
    )
    
