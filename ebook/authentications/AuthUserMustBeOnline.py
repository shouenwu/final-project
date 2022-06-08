from fastapi import Depends
from fastapi import HTTPException

from jose import jwt as JWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



import json as JSON



SECRET_KEY = None
ALGORITHM = None
ACCESS_TOKEN_EXPIRE_MINUTES = None
with open("./configs/token.json", "r") as file_input:

    config = JSON.load(file_input)
    
    SECRET_KEY = config["SECRET_KEY"]
    ALGORITHM = config["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/Login")

async def AuthUserMustBeOnline(token: str = Depends(oauth2_scheme)):

    try:

        jwt_decoded = JWT.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

    except JWT.ExpiredSignatureError:

        raise HTTPException(status_code = 401)

    except JWT.JWSError:

        raise HTTPException(status_code = 400)
    
    except JWT.JWTError:

        raise HTTPException(status_code = 500)

    return {"id": jwt_decoded.get("id"),
            "role": jwt_decoded.get("role")}
