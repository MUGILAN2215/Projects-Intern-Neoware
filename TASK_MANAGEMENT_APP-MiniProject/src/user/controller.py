from src.user.dtos import UserSchema,LoginUser
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException,status,Request
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime,timedelta,timezone
from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def registerUser(body:UserSchema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400,"The UserName Already Existed")

    is_user_email=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user_email:
        raise HTTPException(400,"The Email is Alraedy Existed")

    hash_password=get_password_hash(body.password)

    new_user=UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def login_user(body:LoginUser,db:Session):
    user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="UserName is wrong")

    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You Entered Wrong Password")

    exp_time=datetime.now(timezone.utc)+timedelta(minutes=1)

    token=jwt.encode({"user_id":user.id,"exp":exp_time},settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    
    
    
    return {"token": token}

#
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