from pydantic import BaseModel, ConfigDict, EmailStr

from fast_training.models import TodosState


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


# Classe criada para tipificar o Token extraido JWT e garantir o campo username de identificação
class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodosState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]
