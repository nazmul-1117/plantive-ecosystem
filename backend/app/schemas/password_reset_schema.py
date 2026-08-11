from pydantic import BaseModel, EmailStr, Field, model_validator

class ForgotPasswordRequestSchema(BaseModel):
    email: EmailStr

class ForgotPasswordResponseSchema(BaseModel):
    status: bool
    details: str

class ResetPasswordRequestSchema(BaseModel):
    new_password: str = Field(min_length=6)
    confirm_new_password: str

    @model_validator(mode="after")
    def passwords_match(self):
       if self.new_password != self.confirm_new_password:
           raise ValueError("Password do not match")

       return self


class ResetPasswordResponseSchema(BaseModel):
    status: bool
    details: str