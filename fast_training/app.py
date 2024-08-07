from http import HTTPStatus

from fastapi import FastAPI

from fast_training.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_wt_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_wt_id)

    return user_wt_id


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


# at1:17:30 #3
#mhfch