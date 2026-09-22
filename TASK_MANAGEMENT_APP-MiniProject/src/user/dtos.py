from pydantic import BaseModel

class UserSchema(BaseModel):
    #id:int
    name:str
    username:str
    password:str
    email:str


class UserResponseSchema(BaseModel):
    id:int
    name:str
    username:str
    email:str


class LoginUser(BaseModel):
    username:str
    password:str

class LoginResponse(BaseModel):
    token:str