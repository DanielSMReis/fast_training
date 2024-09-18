from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # para facilitar a resonstrução dos modelos do pydantic durante os testes
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]



#  Criado meramente para ter uma documentação acerca do Tonken
class Token(BaseModel):
    access_token: str
    token_type: str
