from pydantic import BaseModel, model_validator, Field

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    confirm_new_password: str

    @model_validator(mode="after")
    def passwords_match(self):
       if self.new_password != self.confirm_new_password:
           raise ValueError("New passwords do not match")

       if self.old_password == self.new_password:
           raise ValueError(
               "New password must be different from the old password"
           )

       return self


class ChangePasswordResponse(BaseModel):
    status: bool
    details: str