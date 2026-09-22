from fastapi import FastAPI
from src.utils.db import Base,engine
from src.tasks.models import TaskModel
from src.tasks.router import router
from src.user.router import userRouter
from src.user.models import UserModel
from src.utils.helpers import is_authenticated




Base.metadata.create_all(engine)
app=FastAPI()

app.include_router(router)
app.include_router(userRouter)