from fastapi import APIRouter, Depends, HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from models import Todo
import models
from database import engine, sessionLocal
from pydantic import BaseModel, Field
from  routers import auth
from .auth import get_current_user

router=APIRouter()
models.Base.metadata.create_all(bind=engine)
router.include_router(auth.router)
user_dep=Annotated[dict,Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int= Field(gt=0,lt=10)
    complete: bool

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dep=Annotated[Session, Depends(get_db)]
@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dep,db:db_dep):
    #return db.query(Todo).all()
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    return db.query(Todo).filter(user.get('id')==Todo.owner_id).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def getTodoById(user:user_dep,db:db_dep,todo_id:int=Path(gt=0)):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404,detail="Todo with this id not found.")
    

@router.post("/todo/",status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dep,db:db_dep, todo_request:TodoRequest):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=Todo(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dep, user:user_dep,
                      todoReq:TodoRequest,
                      todo_id:int=Path(gt=0)
                      ):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is None:
        raise HTTPException(status_code=401,detail='Todo not found')
    todo_model.title= todoReq.title
    todo_model.description= todoReq.description
    todo_model.priority =todoReq.priority
    todo_model.complete =todoReq.complete
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dep,db:db_dep,todo_id:int =Path(gt=0)):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo with this id not found")
    db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).delete()
    db.commit()