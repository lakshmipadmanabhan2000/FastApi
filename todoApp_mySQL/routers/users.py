from fastapi import APIRouter, Depends, HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
#from models import Todo
from ..models import Todo,Users
#import models
from ..models import Base
#from database import engine, sessionLocal
from ..database import engine,sessionLocal
from pydantic import BaseModel, Field
#from  routers import auth
from ..routers import auth
from .auth import get_current_user
from passlib.context import CryptContext

router=APIRouter(prefix='/users',tags=['users'])
#models.Base.metadata.create_all(bind=engine)
user_dep=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dep=Annotated[Session, Depends(get_db)]

@router.get('/',status_code=status.HTTP_200_OK)
async def get_users(user:user_dep,db:db_dep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authenticated")
    return db.query(Users).filter(Users.id==user.get('id')).all()

class UserVerification(BaseModel):
    password:str
    new_password:str
@router.put('/password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dep,db:db_dep,userVerify:UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authenticated")
    user_model=db.query(Users).filter(user.get('id')==Users.id).first()
    if not bcrypt_context.verify(userVerify.password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authenticated")
    user_model.hashed_password=bcrypt_context.hash(userVerify.new_password)
    db.add(user_model)
    db.commit()
@router.put('/phonenumber',status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dep,db:db_dep,userPhNo:str):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Not authorised')
    user_model=db.query(Users).filter(user.get('id')==Users.id).first()
    user_model.phone_number=userPhNo
    db.add(user_model)
    db.commit()