from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'hello world'}


# at57:49#1
