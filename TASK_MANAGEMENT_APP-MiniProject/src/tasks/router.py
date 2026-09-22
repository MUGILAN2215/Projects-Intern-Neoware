from fastapi import APIRouter,Depends,status
from src.tasks import controller
from src.tasks.dtos import TaskSchema,TaskResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.user.models import UserModel


router = APIRouter(prefix="/tasks")

@router.get("/all",status_code=status.HTTP_200_OK,response_model=List[TaskResponseSchema])
def get_tasks(db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.getTasks(db)


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=TaskResponseSchema)
def get_task(id: int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.get_one_tasks(id,db)

@router.post("/create",status_code=status.HTTP_201_CREATED,response_model=TaskResponseSchema)
def create_task(body:TaskSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.createTask(body,db)

@router.put("/{id}",status_code=status.HTTP_201_CREATED,response_model=TaskResponseSchema)
def update_tasks(id:int,body:TaskSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.update_tasks(body,id,db)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.delete_tasks(id,db)



