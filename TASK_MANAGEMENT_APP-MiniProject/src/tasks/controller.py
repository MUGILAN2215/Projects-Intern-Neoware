from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def createTask(body:TaskSchema,db:Session):
    data=body.model_dump()
    new_tasks=TaskModel(title=data["title"],description=data["description"],is_completed=data["is_completed"])
    db.add(new_tasks)
    db.commit()
    db.refresh(new_tasks)
    #return {"status":"TaskCreated Successfully...","data":new_tasks}
    return new_tasks

def getTasks(db:Session):
    tasks=db.query(TaskModel).all()
    #return {"status":"Returning All Tasks","data":tasks}
    return tasks

def get_one_tasks(task_id:int,db:Session):
    one_task=db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,"The Task ID is not found")
    #return {"status":"The Task is Fetched" ,"data":one_task}
    return one_task

def update_tasks(body:TaskSchema,task_id:int,db:Session):
    one_task=db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,"The Task ID is not found")
    data=body.model_dump()
    for field,value in data.items():
        setattr(one_task,field,value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    #return {"Status":"Tasks Updated Successfully","data":one_task}
    return one_task

def delete_tasks(task_id:int,db:Session):
    one_task=db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,"The Task ID is not found")
    db.delete(one_task)
    db.commit()

    #return f"The Task with the ID {task_id} is deleted Successfully"
    return None