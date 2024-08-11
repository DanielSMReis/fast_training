from http import HTTPStatus

from fastapi import FastAPI, HTTPException

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


# exercicio: coletando um usuario unico
@app.get('/users/{user_id}', response_model=UserPublic)
def read_one_user(user_id: int):
    user_wt_id = database[user_id - 1]
    return {'username': user_wt_id.username, 'email': user_wt_id.email, 'id': user_wt_id.id}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not Found')
    user_wt_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_wt_id

    return user_wt_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not Found')

    del database[user_id - 1]

    return {'message': 'User Deleted'}


# at10849 #4
