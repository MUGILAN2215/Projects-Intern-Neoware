from src.user.dtos import UserSchema,LoginUser
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException,status,Request,Depends
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime,timedelta,timezone
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db



def is_authenticated(request:Request,db:Session=Depends(get_db)):
    try:
        token=request.headers.get("authorization")
        
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You Are UnAuthorized")

        token = token.split(" ")[-1]

        data = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
        user_id=data.get("user_id")
        exp_time=int(data.get("exp"))

        curr_time=datetime.now().timestamp()
        print(curr_time-exp_time)

        if curr_time>exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You Are UnAuthorized")

        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You Are UnAuthorized")
        
        
        return user

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You Are UnAuthorized")