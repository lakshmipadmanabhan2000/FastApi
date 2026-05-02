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

router=APIRouter(prefix='/admin',tags=['admin'])
models.Base.metadata.create_all(bind=engine)
user_dep=Annotated[dict,Depends(get_current_user)]


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dep=Annotated[Session, Depends(get_db)]

@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(db:db_dep,user:user_dep):
    if(user is None or user.get('role')!='admin'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not authorized')
    return db.query(Todo).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dep,db:db_dep,todo_id:int=Path(gt=0)):
    if(user is None or user.get('role')!='admin'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not authorized')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo with this id not found")
    db.query(Todo).filter(Todo.id==todo_id).delete()
    db.commit()