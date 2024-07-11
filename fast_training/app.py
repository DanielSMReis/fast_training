from http import HTTPStatus

from fastapi import FastAPI

from fast_training.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


# at57:49#1
