from pydantic import BaseModel, Field

class UserSchema(BaseModel):
  id: int = Field(gt=0)
  name: str = Field(min_length=5, max_length=255)
  email: str = Field(min_length=5, max_length=255)
  mobile_number: int = Field(gt=0)
  user_type: str = Field(min_length=5, max_length=255)
  country: str = Field(min_length=5, max_length=255)
  created_at: str
  updated_at: str
  