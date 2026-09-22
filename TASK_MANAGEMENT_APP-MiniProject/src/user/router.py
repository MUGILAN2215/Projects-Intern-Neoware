from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status,Request
from src.user.dtos import UserSchema,UserResponseSchema,LoginUser,LoginResponse
from src.utils.db import get_db
from src.user import controller

userRouter = APIRouter(prefix="/user")

@userRouter.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def registerUser(body:UserSchema,db:Session=Depends(get_db)):
    return controller.registerUser(body,db)

@userRouter.post("/login",status_code=status.HTTP_202_ACCEPTED,response_model=LoginResponse)
def loginUser(body:LoginUser,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

# @userRouter.get("/is_auth")
# def is_auth(request:Request,db:Session=Depends(get_db)):
#     return controller.is_authenticated(request,db)
