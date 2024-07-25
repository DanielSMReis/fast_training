from http import HTTPStatus

from fastapi import FastAPI

from fast_training.schemas import UserSchema, Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserSchema)
def create_user(user:UserSchema):
    return user
# at05:49#3
