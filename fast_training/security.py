from datetime import datetime, timedelta
from jwt import encode, decode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

SECRET_KEY = 'secret-key-will-change'
ALGORITHM = 'HS256'
ACCESSS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

'''

'''

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESSS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp':expire})
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt